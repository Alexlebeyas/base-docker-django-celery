from copy import copy
from django import forms as django_forms
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from . import validators

__author__ = 'philippe'


class EmailField(django_forms.EmailField):
    default_error_messages = {
        'required': _('The email is required.'),
    }


class PasswordField(django_forms.CharField):
    default_validators = [validators.validate_password]
    default_error_messages = {
        'required': _('The password is required.'),
    }

    def __init__(self, mask="", *args, **kwargs):
        self.mask = mask
        # Override widget value
        kwargs['widget'] = django_forms.PasswordInput
        super().__init__(*args, **kwargs)


class FirstNameField(django_forms.CharField):
    default_error_messages = {
        'required': _('The first name is required.')
    }


class LastNameField(django_forms.CharField):
    default_error_messages = {
        'required': _('The last name is required.')
    }


class AgeField(django_forms.IntegerField):
    default_error_messages = {
        'required': _('The age is required.'),
        'invalid': _('Enter an integer.'),
    }


class MaskWidget(django_forms.TextInput):
    template = "nixa_fields/widget_mask.html"

    def render(self, name, value, attrs=None):
        context = copy(self.attrs)
        if attrs:
            context.update(attrs)

        if attrs.get('class'):
            context['class'] = "%s nixa-fields-mask" % attrs.get('class')
        else:
            context['class'] = "nixa-fields-mask"

        context['vendor_url'] = static('js/jquery.mask.min.js')

        context['name'] = name
        context['value'] = value
        return get_template(self.template).render(context)

    class Media:
        js = ('js/mask_widget.js', )


class MaskField(django_forms.CharField):
    def __init__(self, mask="", *args, **kwargs):
        self.mask = mask
        # Override widget value
        kwargs['widget'] = MaskWidget
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(MaskField, self).widget_attrs(widget)
        attrs['mask_value'] = self.mask
        return attrs


class PhoneField(MaskField):
    default_error_messages = {
        'required': _('The phone is required.'),
    }


class PostalCodeField(MaskField):
    default_error_messages = {
        'required': _('The postal code is required.'),
    }
