from django.conf import settings

__author__ = 'snake'

if settings.DEBUG:
    from django.conf.urls import url
    from . import views

    urlpatterns = [
        url('^$', views.template_list, name='email_template_list'),
        url('^(?P<pk>.+?)/$', views.template_single, name='email_template_single'),
    ]
else:
    urlpatterns = []
