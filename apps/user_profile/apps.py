from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserProfileConfig(AppConfig):
    name = 'apps.user_profile'
    verbose_name = _('Users')

    def ready(self):
        import apps.user_profile.signals
