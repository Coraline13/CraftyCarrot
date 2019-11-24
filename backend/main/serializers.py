import copy
from collections import OrderedDict

from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import get_attribute


class FlatNestedSerializerMixin(serializers.ModelSerializer):
    _flattened_fields = {}

    def get_fields(self):
        fields = type(self)._declared_fields
        flattened_fields = getattr(type(self), '_flattened_fields', {})
        new_fields = OrderedDict()
        meta = getattr(self, 'Meta', None)

        flatten_fields = getattr(meta, 'flatten_fields', {})
        for field_name, field in fields.items():
            if field_name in flatten_fields:
                nested_field_names = flatten_fields[field_name]
                for nested_field_name in nested_field_names:
                    exclude = getattr(self.Meta, 'exclude', ())
                    include = getattr(self.Meta, 'fields', ()) if not exclude else serializers.ALL_FIELDS
                    if nested_field_name in exclude:
                        continue
                    if include != serializers.ALL_FIELDS and nested_field_name not in include:
                        continue

                    # deepcopy on a serializer field actually creates a new instance with ._args and ._kwargs
                    src_field = field.fields[nested_field_name]
                    nested_kwargs = dict(src_field._kwargs)
                    nested_kwargs['source'] = field_name + '.' + (src_field.source or nested_field_name)
                    if nested_field_name in getattr(meta, 'read_only_fields', ()):
                        nested_kwargs['read_only'] = True
                    nested_kwargs.update(getattr(meta, 'extra_kwargs', {}).get(nested_field_name, {}))

                    orig_kwargs = src_field._kwargs
                    try:
                        src_field._kwargs = nested_kwargs
                        nested_field = copy.deepcopy(src_field)
                        new_fields[nested_field_name] = nested_field
                    finally:
                        src_field._kwargs = orig_kwargs
                flattened_fields[field_name] = type(field), (field.source or field_name)
            else:
                new_fields[field_name] = field

        type(self)._declared_fields = new_fields
        type(self)._flattened_fields = flattened_fields
        return super().get_fields()

    def _update_flattened_field(self, validated_data, instance=None, related_objects=None):
        assert not (instance and related_objects), "cannot pass both instance and related_objects"
        for field_name, (serializer_class, source) in self._flattened_fields.items():
            if field_name in validated_data:
                partial = self.partial
                try:
                    obj = get_attribute(instance, source.split('.'))
                except (AttributeError, KeyError):
                    obj = get_attribute(related_objects, source.split('.'))
                    partial = True
                except (AttributeError, KeyError):
                    obj = None

                serializer = serializer_class(
                    instance=obj, data=validated_data.pop(field_name),
                    context=self.context, partial=partial
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

    @transaction.atomic
    def update(self, instance, validated_data):
        self._update_flattened_field(validated_data, instance=instance)
        return super().update(instance, validated_data)
