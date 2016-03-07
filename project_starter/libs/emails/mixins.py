from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.utils.six import with_metaclass
from django.utils.translation import ugettext_lazy as _
from .settings import USER_LANG_FIELD, USER_ACTIVE_FIELD

__author__ = 'snake'


class EmailMixinMeta(ModelBase):
    def __new__(mcs, name, bases, attrs):
        mcs.replace(attrs, '_lang', USER_LANG_FIELD)
        mcs.replace(attrs, '_can_receive_emails', USER_ACTIVE_FIELD)
        return ModelBase(name, bases, attrs)

    @staticmethod
    def replace(attrs, field_from, field_to):
        try:
            attrs[field_to] = attrs[field_from]
            del attrs[field_from]
        except KeyError:
            pass


class EmailMixin(with_metaclass(EmailMixinMeta, models.Model)):
    _lang = models.CharField(
        _('Email Language'),
        max_length=8,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    _can_receive_emails = models.BooleanField(
        _('Wants to receive emails'),
        default=True,
    )

    class Meta:
        abstract = True
