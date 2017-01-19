import re

from django.utils.translation import ugettext_lazy as _

__author__ = 'philippe'


class PasswordLevel(object):
    DEV, PROD_LOW, PROD_HIGH = range(3)

    messages = {
        DEV: _('Enter a valid password. Only one character needed.'),
        PROD_LOW: _('Enter a valid password. Minimum 8 characters. At least one digit and one letter.'),
        PROD_HIGH: _('Enter a valid password. Minimum 12 characters. At least one digit, one uppercase, '
                     'one lowercase and one special character, like #!?&*()_=~')
    }


class CreditCardsConstant(object):
    MASTERCARD, VISA, AMERICAN_EXPRESS = range(3)

    CC_CHOICE = (
        (MASTERCARD, 'MasterCard'),
        (VISA, 'Visa'),
        (AMERICAN_EXPRESS, 'American Express'),
    )

    CC_PATTERNS = {
        MASTERCARD: '^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$',
        VISA: '^4[0-9]{12}(?:[0-9]{3})?$',
        AMERICAN_EXPRESS: '^3[47][0-9]{13}$'
    }

    @staticmethod
    def get_cc_type(cc_number):
        c = CreditCardsConstant()
        number = str(cc_number).replace(' ', '').replace('-', '')
        type = None

        for k, regex in c.CC_PATTERNS.items():
            if re.match(regex, number):
                type = k
                break

        if type == None:
            raise ValueError('Credit card number is invalid, make sure the credit card value is clean.')

        return type
