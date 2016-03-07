from django.conf import settings

__author__ = 'snake'


USER_EMAIL_FIELD = getattr(settings, 'EMAIL_USER_EMAIL_FIELD', 'email')
USER_LANG_FIELD = getattr(settings, 'EMAIL_USER_LANG_FIELD', 'lang')
USER_ACTIVE_FIELD = getattr(settings, 'EMAIL_USER_ACTIVE_FIELD', 'can_receive_emails')
