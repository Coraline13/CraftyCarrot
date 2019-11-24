from django.contrib import admin
from django.contrib.admin import FieldListFilter
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.utils import get_model_from_relation
from django.core.exceptions import ValidationError
from django.db.models.fields.related import RelatedField
from django.utils.html import escape, format_html
from rest_framework.reverse import reverse


def admin_link_field(model, field_name):
    meta = model._meta

    def link_func(self, obj):
        val = getattr(obj, field_name)
        buyer_url = reverse(f"admin:{meta.app_label}_{meta.model_name}_change", args=(val.id,))
        return format_html('<a href="{}">{}</a>', buyer_url, escape(val))

    link_func.__name__ = ''
    link_func.allow_tags = True
    link_func.short_description = meta.get_field(field_name).verbose_name
    link_func.admin_order_field = field_name

    return link_func


class MultipleChoiceListFilter(admin.SimpleListFilter):
    """Stolen from https://github.com/ctxis/django-admin-multiple-choice-list-filter."""
    template = 'xtec/admin/multiple-choice-list-filter.html'

    def lookups(self, request, model_admin):
        """
        Must be overridden to return a list of tuples (value, verbose value)
        """
        raise NotImplementedError(
            'The MultipleChoiceListFilter.lookups() method must be overridden to '
            'return a list of tuples (value, verbose value).'
        )

    def values(self):
        return self.value().split(',') if self.value() else []

    def choices(self, changelist):

        def amend_query_string(include=None, exclude=None):
            selections = self.values()
            if include and include not in selections:
                selections.append(include)
            if exclude and exclude in selections:
                selections.remove(exclude)
            if selections:
                csv = ','.join(selections)
                return changelist.get_query_string({self.parameter_name: csv})
            else:
                return changelist.get_query_string(remove=[self.parameter_name])

        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': 'All',
            'reset': True,
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': str(lookup) in self.values(),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'include_query_string': amend_query_string(include=str(lookup)),
                'exclude_query_string': amend_query_string(exclude=str(lookup)),
                'display': title,
            }


class MultipleChoiceFieldListFilter(FieldListFilter, MultipleChoiceListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if hasattr(field, 'verbose_name'):
            self.title = field.verbose_name
        else:
            other_model = get_model_from_relation(field)
            self.title = other_model._meta.verbose_name

    @property
    def parameter_name(self):
        if isinstance(self.field, RelatedField):
            return '%s__%s' % (self.field_path, self.field.target_field.name)

        return self.field_path

    def lookups(self, request, model_admin):
        return self.field.get_choices(include_blank=False)

    def queryset(self, request, queryset):
        if self.values():
            try:
                return queryset.filter(**{f'{self.parameter_name}__in': self.values()})
            except (ValueError, ValidationError) as e:
                # Fields may raise a ValueError or ValidationError when converting
                # the parameters to the correct type.
                raise IncorrectLookupParameters(e)

        return queryset
