from __future__ import unicode_literals, print_function
import re
from django.db import models
from django.utils.translation import ugettext_lazy as _

__author__ = 'snick'

imply = lambda a, b: (not a) or b
re_compile = lambda r: re.compile(r, re.DOTALL | re.MULTILINE | re.IGNORECASE)


class ModelValuesIterator(object):
    """
        Iterator for a model. Simulate Model.objects.values() seperated into
        batches to avoid making one huge query of all the database table.
    """

    def __init__(self, model, batch_size=1000):
        self.model_pk = model._meta.pk.name
        self.qs = model.objects.order_by(self.model_pk).values()
        self.batch_size = batch_size
        self.last_pk = None

    def __iter__(self):
        result_size = self.batch_size

        while result_size == self.batch_size:
            objects = self.query_objects()

            for obj in objects:
                yield obj

            result_size = len(objects)

            try:
                self.last_pk = objects[-1][self.model_pk]
            except IndexError:
                pass

    def get_qs(self):
        qs = self.qs

        if self.last_pk is not None:
            qs = qs.filter(pk__gt=self.last_pk)

        return qs

    def query_objects(self):
        return list(self.get_qs()[:self.batch_size])


class ProgressCounter(object):
    def __init__(self, total, msg='%(cursor)s / %(total)s', interval=100, output=print):
        self.total = total
        self.msg = msg
        self.interval = interval
        self.output = output
        self.cursor = 0

    def inc(self, try_print=True):
        self.cursor += 1

        if try_print:
            self.try_print()

    def try_print(self):
        if not self.cursor % self.interval:
            self.print()

    def print(self):
        self.output(self.msg % {
            'cursor': self.cursor,
            'total': self.total,
        })


def slice_text(text, max_length):
    """
        Can be registered as filter
    """

    if len(text) <= max_length:
        return text

    try:
        return '%s ...' % text[:text.rindex(' ', 0, max_length)]
    except ValueError:
        return text[:max_length]


class TimeStampMixin(models.Model):
    created = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        abstract = True

