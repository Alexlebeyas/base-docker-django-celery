from django.conf.urls import url
from . import views

__author__ = 'snake'


urlpatterns = (
    url(r'^$', views.home, name='home'),
)

urlpatterns = (
    url(r'^error', views.error, name='error'),
)