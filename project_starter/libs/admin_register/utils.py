from __future__ import print_function
from django.contrib import admin
from django.db import models
from django.db.models import Field

__author__ = 'snake'

# Restricted fields

list_display_restricted_fields = (
    models.OneToOneField,
    models.TextField,
    models.ManyToManyField,
)

search_restricted_fields = (
    models.AutoField,
    models.ForeignKey,
    models.ManyToManyField,
)


def get_related_attribute(relation):
    """
        Follow related fields define as strings: "foreignkey__attribute"
    """
    attrs = relation.split('__')

    def w(obj):
        related_attr = obj
        for attr in attrs:
            related_attr = getattr(related_attr, attr)
        return str(related_attr)

    w.short_description = ' '.join(attr.title() for attr in attrs)
    return w


def inline_factory(inline_type, model, **kwargs):
    kwargs.update({'model': model})
    return type('%s_inline' % model.__name__, (inline_type, ), kwargs)


def stacked_inline_factory(model, **kwargs):
    return inline_factory(admin.StackedInline, model, **kwargs)


def tabular_inline_factory(model, **kwargs):
    return inline_factory(admin.TabularInline, model, **kwargs)


class AdminRegister(object):

    def __init__(self, model):
        self.model = model
        self.admin_model = None

    def __call__(self, model_admin):
        """
            Decorator of admin.ModelAdmin

            Add many features to ``model_admin`` and register
            it to the admin site
        """

        self.admin_model = model_admin
        self.set_inlines()

        # Set all fields read only
        if hasattr(self.admin_model, 'all_fields_read_only'):
            read_only_fields = self.get_all_fields()
            self.admin_model.readonly_fields = read_only_fields

        if not self.admin_model.search_fields:
            self.set_search_fields()

        if self.admin_model.list_display == ('__str__', ):
            self.set_list_display_from_meta()
            self.set_list_display_extra_fields()

        self.set_list_display_relations()

        admin.site.register(self.model, model_admin)
        return model_admin

    def get_meta_fields(self, restricted_fields):
        """
            Get meta fields of self.model and exclude restricted_fields
        """

        return [f.name for f in self.model._meta.fields if not isinstance(f, restricted_fields)]

    def set_list_display_from_meta(self):
        exclude_fields = getattr(self.admin_model, 'list_display_exclude', [])
        self.admin_model.list_display = []

        for field in self.get_meta_fields(list_display_restricted_fields):
            if field not in exclude_fields:
                self.admin_model.list_display.append(field)

    def set_list_display_extra_fields(self):
        extra_fields = getattr(self.admin_model, 'list_display_add', [])

        for field in extra_fields:
            self.admin_model.list_display.append(field)

    def set_list_display_relations(self):
        """
            Transform the strings representing related fields into
            callables that the admin class can use
        """

        new_list_display = []

        for attr in self.admin_model.list_display:
            try:
                if '__' in attr:
                    attr = get_related_attribute(attr)
            except TypeError:
                pass

            new_list_display.append(attr)

        self.admin_model.list_display = new_list_display

    def set_search_fields(self):
        self.admin_model.search_fields = self.get_meta_fields(search_restricted_fields)

    def set_inlines(self):
        """
            Make inline classes with models from 'stacked_inlines' and 'tabular_inlines'
        """

        inlines = getattr(self.admin_model, 'inlines', [])
        inlines = list(inlines)  # bug fix

        stacked_inlines = getattr(self.admin_model, 'stacked_inlines', ())
        inlines += (stacked_inline_factory(model) for model in stacked_inlines)

        tabular_inlines = getattr(self.admin_model, 'tabular_inlines', ())
        inlines += (tabular_inline_factory(model) for model in tabular_inlines)

        self.admin_model.inlines = inlines

    def get_all_fields(self):
        """
        Get all fields of the model,
            except related fields
        :return: list of all fields
        """
        fields = []
        for field in self.model._meta.get_fields():
            if issubclass(field.__class__, Field):
                fields.append(field.name)
        return fields
