from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from . import validators
from django.utils.translation import ugettext_lazy as _
from . import forms

__author__ = 'philippe'


default_error_messages = {
    'invalid_choice': _('Value %(value)r is not a valid choice.'),
    'null': _('This field cannot be null.'),
    'blank': _('This field cannot be blank.'),
    'unique': _('%(model_name)s with this %(field_label)s '
                'already exists.'),
    # Translators: The 'lookup_type' is one of 'date', 'year' or 'month'.
    # Eg: "Title must be unique for pub_date year"
    'unique_for_date': _("%(field_label)s must be unique for "
                         "%(date_field_label)s %(lookup_type)s."),
}


class NixaFieldMixin(models.Field):
    """

    To create a new nixa field use the NixaFieldMixin
    and define the custom data dictionnary

    Key needs:
        verbose_name
        form_class => must create a form field
    Key optional:
        max_length
        mask
    """
    custom_data = {}

    def __init__(self, *args, mask=None, **kwargs):
        defaults = {}

        if not args and "verbose_name" not in kwargs:
            args = (self.custom_data.get('verbose_name'),)

        max_length = self.custom_data.get('max_length')
        if max_length:
            defaults.update({
                "max_length": max_length
            })

        default_mask = self.custom_data.get('mask', None)
        self.mask = default_mask
        if mask is not None:
            self.mask = mask

        defaults.update(kwargs)
        super().__init__(*args, **defaults)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.custom_data.get('form_class'),
        }

        if self.mask:
            defaults.update({
                "mask": self.mask
            })

        defaults.update(kwargs)
        return super().formfield(**defaults)


class EmailField(NixaFieldMixin, models.EmailField):
    default_validators = [validators.validate_email]
    description = _("Email address")
    default_error_messages = default_error_messages
    custom_data = {
        'verbose_name': _('Email'),
        'max_length': 254,
        'form_class': forms.EmailField,
    }


class PasswordField(NixaFieldMixin, models.CharField):
    description = _("Password field")
    validators = [validators.validate_password]
    default_error_messages = default_error_messages
    custom_data = {
        'verbose_name': _('Password'),
        'max_length': 128,
        'form_class': forms.PasswordField
    }


class FirstNameField(NixaFieldMixin, models.CharField):
    description = _('First name')
    default_error_messages = default_error_messages
    custom_data = {
        'verbose_name': _('First name'),
        'max_length': 256,
        'form_class': forms.FirstNameField,
    }


class LastNameField(NixaFieldMixin, models.CharField):
    description = _('Last name')
    default_error_messages = default_error_messages
    custom_data = {
        'verbose_name': _('Last name'),
        'max_length': 256,
        'form_class': forms.LastNameField,
    }


class AgeField(NixaFieldMixin, models.PositiveSmallIntegerField):
    description = _('Age')
    default_validators = [
        MinValueValidator(1, _('Enter a valid age value.')),
        MaxValueValidator(125, _('Enter a valid age value.')),
    ]
    custom_data = {
        'verbose_name': _('Age'),
        'form_class': forms.AgeField,
    }


class PhoneField(NixaFieldMixin, models.CharField):
    description = _('Phone number')
    default_validators = [
        RegexValidator(
            regex=r'^1?\d{10,15}$',
            message=_("Enter a valid phone number. Up to 15 digits allowed.")
        )
    ]
    default_error_messages = default_error_messages
    custom_data = {
        'verbose_name': _('Phone'),
        'max_length': 15,
        'form_class': forms.PhoneField,
        'mask': "(000) 000-0000"
    }


class PostalCodeField(NixaFieldMixin, models.CharField):
    description = _('Postal code')
    default_validators = [
        RegexValidator(
            regex=r'^[\d\w]{3,10}$',
            message=_("Enter a valid postal code.")
        )
    ]
    default_error_messages = default_error_messages
    custom_data = {
        'verbose_name': _('Postal code'),
        'max_length': 10,
        'form_class': forms.PostalCodeField,
        'mask': 'Z0Z 0Z0'
    }
