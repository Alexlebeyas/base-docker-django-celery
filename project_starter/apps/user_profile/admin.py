from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile
import nixa_users


User = get_user_model()

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(nixa_users.admin.UserAdmin):
    inlines = nixa_users.admin.UserAdmin.inlines + [ProfileInline]
