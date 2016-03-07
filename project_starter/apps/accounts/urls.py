from __future__ import absolute_import
from django.conf.urls import url

__author__ = 'Philippe'

urlpatterns = (

    # PASSWORD RETRIEVAL CYCLE!
    url(r'^password/reset/send/$', 'django.contrib.auth.views.password_reset', {
        'template_name': 'accounts/password_reset_send.html',
        'post_reset_redirect': '/accounts/password/send/done/',
    }, name='accounts_password_reset'),
    url(r'^password/send/done/$', 'django.contrib.auth.views.password_reset_done', {
        'template_name': 'accounts/password_send_done.html',
    }),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm', {
            'post_reset_redirect': '/accounts/password/done/',
            'template_name': 'accounts/password_reset.html',
        }, name='password_reset_confirm'),
    url(r'^password/done/$', 'django.contrib.auth.views.password_reset_complete', {
        'template_name': 'accounts/password_reset_done.html',
    }),
)