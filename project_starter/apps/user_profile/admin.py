from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile
import nixausers


User = get_user_model()

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(nixausers.admin.UserAdmin):
    inlines = nixausers.admin.UserAdmin.inlines + [ProfileInline]
