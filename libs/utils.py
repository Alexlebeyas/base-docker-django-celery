from __future__ import unicode_literals, print_function
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampMixin(models.Model):
    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True


def serialize_ajax_errors(*forms):
    errors = {}
    for form in forms:
        for k, v in json.loads(form.errors.as_json()).items():
            new_key = "-".join([form.prefix, k]) if form.prefix else k
            errors[new_key] = v
    return json.dumps(errors)
