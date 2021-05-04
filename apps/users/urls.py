from __future__ import absolute_import

from django.contrib.auth import views as auth_views
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [
    path(_('register/'), views.register, name='register'),
    path(_('login/'), views.login, name='login'),
    path(_('check_code/'), views.checkpartnercode, name='checkcode'),
    path(_('logout/'), views.logout, name='logout'),
    path(_('newsletter'), views.add_to_newsletter, name='subscribe_newsletter'),
    path(_('reset-password/'), auth_views.PasswordResetView.as_view(), name='reset_password'),
    path(_('reset-password-ajax/'), views.CustomPasswordResetView.as_view(), name='reset_password_ajax'),
    path(_('reset-password-sent/'), auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(_('reset/<uidb64>/<token>'), auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(_('reset-password-complete/'), auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path(_('edit-user-address/'), views.edit_user_address, name='edit_user_address'),
    path(_('partner/autocomplete/'), views.autocompletePartner, name='partnerautocomplete'),
    path(_('address-ajax/'), views.ChangeAddress.as_view(), name='change_address'),
]

