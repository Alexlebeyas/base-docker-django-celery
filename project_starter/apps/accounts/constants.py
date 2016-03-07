from django.utils.translation import ugettext_lazy as _

__author__ = 'Philippe'


authentification_set = (_('Authentification'), {'fields': (
    'email',
    'password1',
    'password2',
)})

personal_info_set = (_('Personal info'), {'fields': (
    'first_name',
    'last_name',
)})


options_set = (_('Options'), {'fields': (
    'lang',
    'can_receive_emails',
)})

admin_set = (_('Admin'), {'fields': (
    'is_active',
    'is_staff',
    'is_superuser',
    'last_login',
    'date_joined',
    'user_permissions',
    'groups',
)})


ALL_FIELDSETS = (authentification_set, personal_info_set, options_set, admin_set)
ALL_AUTHOR_FIELDSETS = (authentification_set, personal_info_set, options_set,
                        admin_set)
