from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import translation
from django.utils.six import wraps
from .registry import templates

__author__ = 'snake'


def language_middleware(view):
    def _wrapper(request, *args, **kwargs):
        post_language = request.GET.get('email_change_language')
        if post_language:
            response = HttpResponseRedirect(request.path)
            response.set_cookie('email_language', post_language)
            return response
        cookie_language = request.COOKIES.get('email_language')
        if cookie_language:
            translation.activate(cookie_language)
        return view(request, *args, **kwargs)
    return wraps(view)(_wrapper)


@language_middleware
def template_list(request):
    return TemplateResponse(request, 'emails/template_list.html', {
        'templates': templates.values(),
    })


@language_middleware
def template_single(request, pk):
    return TemplateResponse(request, 'emails/template_single.html', {
        'template': templates[pk],
    })