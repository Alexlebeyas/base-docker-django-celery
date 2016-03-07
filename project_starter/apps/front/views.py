from django.template.response import TemplateResponse

__author__ = 'snake'


def home(request):
    return TemplateResponse(request, 'home.html', {
    })