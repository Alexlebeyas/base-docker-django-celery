from copy import copy
from django import forms as django_forms
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from libs.nixa_fields.widgets import MaskWidget

from project_starter.libs.nixa_fields.constants import CreditCardsConstant
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


class CreditCardField(MaskField):
    default_validators=[validators.validate_credit_card]


class CCVerificationField(django_forms.IntegerField):
    default_validators = [validators.validate_ccv]
    cc_errors_messages = {
        'match': _('Le numéro de sécurité ne correspond pas avec votre type carte de crédit')
    }

    widget = MaskWidget(attrs={
        'size': 4,
        'max_length': 4
    })

    # Must be call after the super clean, otherwise you'll get errors and you will be angry >:(
    @staticmethod
    def is_code_match_cc(cc_number, code):
        cc_constant = CreditCardsConstant()
        type = cc_constant.get_cc_type(cc_number)
        return ((type == cc_constant.MASTERCARD or type == cc_constant.VISA) and len(str(code)) == 3) or \
               (type == cc_constant.AMERICAN_EXPRESS and len(str(code)) == 4)


# Example
class CreditCardBaseForm(django_forms.Form):

    credit_card = CreditCardField()
    ccv = CCVerificationField()

    def clean(self):
        cleaned_data = super(CreditCardBaseForm, self).clean()
        credit_card = cleaned_data.get("credit_card")
        cvc = cleaned_data.get("ccv")

        if credit_card and cvc:
            if not CCVerificationField.is_code_match_cc(credit_card, cvc):
                self.add_error("ccv", CCVerificationField.cc_errors_messages['match'])