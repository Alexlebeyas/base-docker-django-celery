from django.apps import AppConfig


class EmailsConfig(AppConfig):
    name = 'libs.emails'
    verbose_name = "Emails"

    def ready(self):
        from .classes import Email
        from .exceptions import EmailException
        from .mixins import EmailMixin
        from .models import EmailSent
