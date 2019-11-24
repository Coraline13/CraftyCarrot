from collections import OrderedDict
from typing import List

import uritemplate
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import CamelCaseJSONFilter, FieldInspector, NotHandled, SwaggerAutoSchema
from drf_yasg.utils import force_real_str, is_list_view, merge_params, force_serializer_instance
from inflection import camelize
from phonenumber_field.serializerfields import PhoneNumberField as PhoneNumberSerializerField
from rest_framework import exceptions, permissions, status
from rest_framework.settings import api_settings
from str2bool import str2bool

from users.permissions import IsNotAuthenticated, IsOpenForSignup


def camelize_path(uri):
    # convert path parameter names to camelCase
    for var in uritemplate.variables(uri):
        var_tag = '{' + var + '}'
        uri = uri.replace(var_tag, camelize(var_tag))

    return uri


def camelize_parameters(parameters: List[openapi.Parameter]):
    for parameter in parameters:
        if parameter.in_ == openapi.IN_PATH:
            parameter.name = camelize(parameter.name, uppercase_first_letter=False)

    return parameters


class XtecSwaggerSchemaGenerator(OpenAPISchemaGenerator):
    def get_operation_keys(self, subpath, method, view):
        keys = super().get_operation_keys(subpath, method, view)
        return [key.replace('partial_update', 'update') for key in keys]

    def get_path_item(self, path, view_cls, operations):
        # move path Parameters to Operation level (down from PathItem level)
        # ng-swagger-gen is dumb
        path_item = super().get_path_item(path, view_cls, operations)
        for method, operation in path_item.operations:
            operation.parameters = camelize_parameters(operation.parameters)
            operation.parameters = merge_params(path_item.parameters, operation.parameters)

        del path_item.parameters
        return path_item

    def get_path_parameters(self, path, view_cls):
        return camelize_parameters(super().get_path_parameters(path, view_cls))

    def get_paths(self, endpoints, components, request, public):
        paths, prefix = super().get_paths(endpoints, components, request, public)
        new_paths = OrderedDict()
        extras = OrderedDict()
        for key, val in paths.items():
            if key.startswith('/'):
                new_paths[camelize_path(key)] = val
            else:
                extras[key] = val

        return openapi.Paths(paths=new_paths, **extras), prefix


class NoSchemaTitleInspector(FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        # remove the `title` attribute of all Schema objects
        if isinstance(result, openapi.Schema.OR_REF):
            try:
                schema = openapi.resolve_ref(result, self.components)
                schema.pop('title', None)
            except Exception:
                pass

        return result


class PhoneNumberInspector(FieldInspector):
    def field_to_swagger_object(self, field, swagger_object_type, use_references, **kwargs):
        SwaggerType, ChildSwaggerType = self._get_partial_types(field, swagger_object_type, use_references, **kwargs)

        if isinstance(field, PhoneNumberSerializerField):
            return SwaggerType(type=openapi.TYPE_STRING, pattern=r'^\+?(?:[0-9]\s*){8,}$', format='phone')

        return NotHandled


drf_generic_error = openapi.Schema('Generic API Error', type=openapi.TYPE_OBJECT, properties={
    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error details'),
    'code': openapi.Schema(type=openapi.TYPE_STRING, description='Error code'),
}, required=['detail'])

drf_validation_error = openapi.Schema('Validation Error', type=openapi.TYPE_OBJECT, properties={
    api_settings.NON_FIELD_ERRORS_KEY: openapi.Schema(
        description='List of validation errors not related to any field',
        type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
    ),
}, additional_properties=openapi.Schema(
    description='A list of error messages for each field that triggered a validation error',
    type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
))


class XtecSwaggerAutoSchema(SwaggerAutoSchema):
    anon_permission_classes = (permissions.AllowAny, IsNotAuthenticated, IsOpenForSignup)
    field_inspectors = [NoSchemaTitleInspector, PhoneNumberInspector, *SwaggerAutoSchema.field_inspectors]

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        if str2bool(self.request.GET.get('postman')):
            operation.summary = getattr(operation, 'summary', '') or operation.operation_id
        return operation

    def get_override(self, name):
        return getattr(self.view, name, None) or self.overrides.get(name, None)

    def get_tags(self, operation_keys=None):
        # allow custom tag name
        tag = self.get_override('swagger_tag')
        tags = [tag] if tag else super().get_tags(operation_keys)
        child_tags = self.get_override('swagger_child_tags') or []
        tags.extend(child_tags)
        return [' > '.join(tags)]

    def get_operation_id(self, operation_keys=None):
        # convert operation ids to camelCase
        return camelize(super().get_operation_id(operation_keys).replace('-', '_'), uppercase_first_letter=False)

    def get_security(self):
        # remove security lock from unauthenticated views
        try:
            perms = self.view.get_permissions()
            if perms and all(isinstance(perm, self.anon_permission_classes) for perm in perms):
                return []
        except Exception:
            pass

        return super().get_security()

    def camelize_error_schema(self, schema):
        camelizer = CamelCaseJSONFilter(self.view, self.path, self.method, self.components, self.request, [])
        if camelizer.is_camel_case():
            camelizer.camelize_schema(schema)

        return schema

    def get_default_response_serializer(self):
        if hasattr(self.view, 'get_response_serializer_class'):
            return force_serializer_instance(self.view.get_response_serializer_class())

        return super().get_default_response_serializer()

    def get_response_serializers(self):
        responses = super().get_response_serializers()
        definitions = self.components.with_scope(openapi.SCHEMA_DEFINITIONS)  # type: openapi.ReferenceResolver

        definitions.setdefault('GenericError', lambda: self.camelize_error_schema(drf_generic_error))
        definitions.setdefault('ValidationError', lambda: self.camelize_error_schema(drf_validation_error))

        if self.get_request_serializer():
            responses.setdefault(status.HTTP_400_BAD_REQUEST, openapi.Response(
                description=force_real_str(exceptions.ValidationError.default_detail),
                schema=openapi.SchemaRef(definitions, 'ValidationError')
            ))

        security = self.get_security()
        if security is None or len(security) > 0:
            responses.setdefault(exceptions.AuthenticationFailed.status_code, openapi.Response(
                description="Authentication credentials were invalid or absent.",
                schema=openapi.SchemaRef(definitions, 'GenericError')
            ))
        if not is_list_view(self.path, self.method, self.view):
            responses.setdefault(exceptions.PermissionDenied.status_code, openapi.Response(
                description="Permission denied.",
                schema=openapi.SchemaRef(definitions, 'GenericError')
            ))
            responses.setdefault(exceptions.NotFound.status_code, openapi.Response(
                description="Object does not exist or caller has insufficient permissions to access it.",
                schema=openapi.SchemaRef(definitions, 'GenericError')
            ))

        return responses
