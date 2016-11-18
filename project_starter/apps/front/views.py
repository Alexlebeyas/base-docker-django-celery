from django.template.response import TemplateResponse

__author__ = 'snake'


def home(request):
    return TemplateResponse(request, 'home.html', {
    })

def sample(request):
    return TemplateResponse(request, 'sample.html', {
    })

def error(request):
    return TemplateResponse(request, 'custom-404.html', {
    })