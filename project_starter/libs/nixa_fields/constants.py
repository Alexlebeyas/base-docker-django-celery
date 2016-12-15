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
