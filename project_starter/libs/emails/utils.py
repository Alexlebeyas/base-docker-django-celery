from django.conf import settings
from django.utils.functional import cached_property

__author__ = 'snake'


def clean_template_name(template):
    """
    Support template names with or without
    the .html extension.
    """
    if not template.endswith('.html'):
        template += '.html'
    return template


def prod_cached_property(func):
    """
    Wraps with property in debug and
    cached_property in prod.
    """
    return property(func) if settings.DEBUG else cached_property(func)
