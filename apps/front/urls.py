from django.urls import path
from . import views

__author__ = 'Alexis'

urlpatterns = (
    path('', views.home, name='home'),
)