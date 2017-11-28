from django.contrib import admin
from django.contrib.auth import get_user_model
from hijack_admin.admin import HijackUserAdminMixin

from .models import Profile
import nixa_users

User = get_user_model()

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(nixa_users.admin.UserAdmin, HijackUserAdminMixin):
    list_display = 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login', 'hijack_field',
    inlines = nixa_users.admin.UserAdmin.inlines + [ProfileInline]
