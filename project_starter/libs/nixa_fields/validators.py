import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from libs.nixa_fields.constants import PasswordLevel, CreditCardsConstant

__author__ = 'philippe'


@deconstructible
class EmailValidator(EmailValidator):
    message = _('Enter a valid email address.')
    # If we want to override
    # code = 'invalid'
    # user_regex = re.compile(
    #     r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
    #     r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
    #     re.IGNORECASE)
    # domain_regex = re.compile(
    #     # max length of the domain is 249: 254 (max email length) minus one
    #     # period, two characters for the TLD, @ sign, & one character before @.
    #     r'(?:[A-Z0-9](?:[A-Z0-9-]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z',
    #     re.IGNORECASE)
    # literal_regex = re.compile(
    #     # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
    #     r'\[([A-f0-9:\.]+)\]\Z',
    #     re.IGNORECASE)
    # domain_whitelist = ['localhost']


validate_email = EmailValidator()


@deconstructible
class PasswordValidator(object):
    code = "invalid"
    password_regexes = {
        PasswordLevel.DEV: re.compile(r"^.$"),
        PasswordLevel.PROD_LOW: re.compile(r"^(?=.*[0-9])(?=.*[a-zA-Z]).{8,}$"),
        PasswordLevel.PROD_HIGH: re.compile(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[#!?&*()_=~]).{12,}$"),
    }
    message = PasswordLevel.messages[PasswordLevel.DEV]
    regex = password_regexes[PasswordLevel.DEV]

    def __init__(self, code=None):
        try:
            level = settings.PASSWORD_LEVEL
        except AttributeError:
            pass
        else:
            self.message = PasswordLevel.messages.get(level)
            self.regex = self.password_regexes.get(level)
        if code is not None:
            self.code = code

    def __call__(self, value):
        value = force_text(value)

        if not value:
            raise ValidationError(self.message, code=self.code)

        if not self.regex.match(value):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, PasswordValidator) and
            (self.regex == other.regex) and
            (self.message == other.message) and
            (self.code == other.code)
        )


validate_password = PasswordValidator()


@deconstructible
class CreditCardValidator(object):
    code = "invalid"
    messages = {
        'invalid_card': '%s%s' % (_('Veuillez entrer une carte '),
                                  ', '.join([str(x[1]) for x in CreditCardsConstant.CC_CHOICE])),
        'invalid_number': _('Veuillez entrer un numero de carte valide'),
    }

    def __init__(self, code=None):
        if code is not None:
            self.code = code

    def __call__(self, value):
        number = force_text(str(value))
        if not self.is_valid_number(value=number):
            print('__call__ %s' % number)
            raise ValidationError(self.messages['invalid_number'], code=self.code)

        if not self.is_valid_card(value=number):
            raise ValidationError(self.messages['invalid_card'], code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            (self.messages == other.message)
            and (self.code == other.code)
        )

    def strip_to_number(self, value):
        return value.replace(' ', '').replace('-', '')

    def is_valid_card(self, value):
        number = self.strip_to_number(value=value)
        is_valid = False

        for k, regex in CreditCardsConstant.CC_PATTERNS.items():
            if re.match(regex, number):
                is_valid = True
                print(k)
                break

        return is_valid

    def is_valid_number(self, value):
        number = self.strip_to_number(value=value)
        return bool(re.search('^[0-9]{13,16}$', number))


validate_credit_card = CreditCardValidator()


def validate_ccv(value):
    if not bool(re.search('^[0-9]{3,4}$', str(value))):
        raise ValidationError(_('Le code de sécurité que vous avez fourni est invalide'), code='invalid')
