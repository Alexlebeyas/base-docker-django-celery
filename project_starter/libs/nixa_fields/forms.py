from calendar import monthrange
from datetime import date
from django import forms as django_forms
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from libs.nixa_fields.widgets import MaskWidget
from libs.nixa_fields.constants import CreditCardsConstant
from libs.nixa_fields.widgets import CCExpirationWidget
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


class CreditCardField(django_forms.CharField):
    default_validators = [validators.validate_credit_card]
    widget = MaskWidget(attrs={
        'max_length': 19
    })

    def to_python(self, value):
        if value in self.empty_values:
            return ''
        return smart_text(value.replace(' ', '').replace('-', ''))


class CCVerificationField(django_forms.CharField):
    default_validators = [validators.validate_ccv]
    cc_errors_messages = {
        'match': _('Le numéro de sécurité ne correspond pas avec votre type carte de crédit')
    }

    widget = MaskWidget(attrs={
        'max_length': 4
    })

    # Must be called after the super() clean, otherwise you'll get errors and you will be angry >:(
    @staticmethod
    def is_code_match_cc(cc_number, code):
        cc_constant = CreditCardsConstant()
        type = cc_constant.get_cc_type(cc_number)
        return ((type == cc_constant.MASTERCARD or type == cc_constant.VISA) and len(str(code)) == 3) or \
               (type == cc_constant.AMERICAN_EXPRESS and len(str(code)) == 4)


class CCExpirationMultiField(django_forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in range(1, 13)]
    EXP_YEAR = [(x, x) for x in range(date.today().year,
                                      date.today().year + 15)]

    default_error_messages = {
        'invalid_month': _('Enter a valid month.'),
        'invalid_year': _('Enter a valid year.'),
        'invalid_date': _('The expiration date you entered is in the past.'),
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            django_forms.ChoiceField(choices=self.EXP_MONTH,
                                     error_messages={'invalid': errors['invalid_month']}),
            django_forms.ChoiceField(choices=self.EXP_YEAR,
                                     error_messages={'invalid': errors['invalid_year']}),
        )
        super(CCExpirationMultiField, self).__init__(fields, *args, **kwargs)
        self.widget = CCExpirationWidget(
            widgets=[fields[0].widget, fields[1].widget],
            attrs={'class': 'nixa-fields-mask form-control'}
        )

    def clean(self, value):
        exp = super(CCExpirationMultiField, self).clean(value)
        if date.today() > exp:
            raise django_forms.ValidationError(self.default_error_messages['invalid_date'])

    def compress(self, data_list):
        if data_list:
            if data_list[1] in django_forms.fields.EMPTY_VALUES:
                raise django_forms.ValidationError(self.default_error_messages['invalid_year'])
            if data_list[0] in django_forms.fields.EMPTY_VALUES:
                raise django_forms.ValidationError(self.default_error_messages['invalid_month'])

            year = int(data_list[1])
            month = int(data_list[0])
            day = monthrange(year, month)[1]
            return date(year, month, day)
        return None


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
