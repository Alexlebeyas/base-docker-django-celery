import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from libs.nixa_fields.constants import PasswordLevel

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
