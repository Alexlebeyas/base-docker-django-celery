from django.conf import settings
from django.utils.importlib import import_module
from .classes import Email

__author__ = 'snake'


def discover_templates():
    for app in settings.INSTALLED_APPS:
        email_templates_module_name = '%s.email_templates' % app
        try:
            email_templates_module = import_module(email_templates_module_name)
        except ImportError as e:
            if 'email_templates' not in str(e):
                raise
            continue
        for attr in dir(email_templates_module):
            obj = getattr(email_templates_module, attr)
            if isinstance(obj, Email):
                yield obj.template, obj


templates = dict(discover_templates())
