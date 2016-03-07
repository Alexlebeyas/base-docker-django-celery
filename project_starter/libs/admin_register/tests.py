from __future__ import absolute_import, print_function
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered
from django.db import models
from django.test import SimpleTestCase
from . import AdminRegister

__author__ = 'snake'


charfield_blank = lambda: models.CharField(default='', blank=True, max_length=100)


class Country(models.Model):
    name = charfield_blank()


class Person(models.Model):
    first_name = charfield_blank()
    last_name = charfield_blank()
    description = models.TextField(default='', blank=True)
    country = models.ForeignKey(Country)

    def get_full_name(self):
        return ' '.join((self.first_name, self.last_name)).title()


def admin_factory(model, **kwargs):
    """
        Re-register the model and create a
        new admin class to reset for each test
    """

    try:
        admin.site.unregister(model)
    except NotRegistered:
        pass
    new_person_admin = type('%sAdmin' % model.__name__, (admin.ModelAdmin, ), kwargs)
    return AdminRegister(model)(new_person_admin)


def person_admin_factory(**kwargs):
    """
        Re-register the model Person
    """

    return admin_factory(Person, **kwargs)


def country_admin_factory(**kwargs):
    """
        Re-register the model Country
    """

    return admin_factory(Country, **kwargs)


class AdminRegisterTest(SimpleTestCase):

    def test_actually_register_in_admin(self):
        self.assertTrue('Trust me..')

        # ok fine..
        # trying to re-register the model `Person` raises `AlreadyRegistered`

        person_admin_factory()
        self.assertRaises(AlreadyRegistered, lambda: admin.site.register(Person))

    def test_list_display_default(self):
        """
            Adds all fields into list_display and leave out TextField, OneToOne, ManyToMany
        """

        person_admin = person_admin_factory()
        self.assertTrue(person_admin.list_display == ['id', 'first_name', 'last_name', 'country'])

    def test_search_fields(self):
        person_admin = person_admin_factory()
        self.assertTrue(person_admin.search_fields == ['first_name', 'last_name', 'description'])

    def test_list_display_no_overwrite(self):
        """
            Custom list_display is not overwritten
        """

        custom_list_display = ['first_name', 'last_name', ]
        person_admin = person_admin_factory(
            list_display=custom_list_display,
        )

        self.assertTrue(person_admin.list_display == custom_list_display)

    def test_related_fields(self):
        """
            Strings with related relations converted into callables
        """

        custom_list_display = ['country__name', ]
        person_admin = person_admin_factory(
            list_display=custom_list_display,
        )

        person = Person(
            country=Country(
                pk=1,  # Since django 1.8, related fields must have a 'pk'.
                name='Snick',
            ),
        )

        # The result of 'country__name' is 'Snick'
        self.assertTrue(person_admin.list_display[0](person) == 'Snick')

        # Not yet implemented
        # Search fields also includes 'country__name'
        # self.assertTrue(person_admin.search_fields[0] == 'country__name' )

    def test_list_display_exclude(self):
        """
            Remove fields in 'list_display_exclude' from list_display
        """

        person_admin = person_admin_factory(
            list_display_exclude='last_name',
        )
        self.assertTrue(person_admin.list_display == ['id', 'first_name', 'country'])

    def test_inlines(self):
        """
            Make inline classes with models from 'stacked_inlines' and 'tabular_inlines'
        """

        country_admin = country_admin_factory(
            stacked_inlines=(Person, ),
            tabular_inlines=(Person, ),
        )

        self.assertTrue(admin.StackedInline in country_admin.inlines[0].__bases__)
        self.assertTrue(admin.TabularInline in country_admin.inlines[1].__bases__)

    def test_list_display_add(self):
        """
            Append fields in 'list_display_add' to list_display
        """

        person_admin = person_admin_factory(
            list_display_add=('get_full_name', ),
        )

        self.assertTrue(person_admin.list_display == ['id', 'first_name', 'last_name', 'country', 'get_full_name'])

    def test_all_fields_read_only(self):
        """
            All fields are set in read_only mode
        """

        person_admin = person_admin_factory(
            all_fields_read_only=True,
        )

        self.assertTrue(person_admin.readonly_fields == ['id', 'first_name', 'last_name', 'description', 'country'])