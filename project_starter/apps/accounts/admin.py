from django.contrib import admin
from django.contrib.auth.models import Group
from libs.admin_register import AdminRegister
from . import models, forms, constants

__author__ = 'snake'

admin.site.unregister(Group)


@AdminRegister(models.User)
class UserAdmin(admin.ModelAdmin):
    form = forms.UserAdminForm
    fieldsets = constants.ALL_FIELDSETS
    list_display = 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login',
    readonly_fields = 'last_login', 'date_joined',
    filter_horizontal = 'groups', 'user_permissions',
