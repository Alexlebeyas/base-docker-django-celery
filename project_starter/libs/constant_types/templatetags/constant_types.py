from django.conf import settings
from django.template import Library
from django.utils.html import escapejs
from django.utils.translation import override

__author__ = 'Philippe'

register = Library()


@register.simple_tag
def choice_dictionary(choices, lang):
    with override(lang):
        dictionary_format = '{value:\'%s\',label:\'%s\'}'
        res = '%s: [%s]' % (lang, ','.join(dictionary_format % (escapejs(k), escapejs(v)) for k, v in choices))
    return res


@register.inclusion_tag('constant_types/_static_structures.html')
def constant_types():
    try:
        constants = settings.CONSTANT_TYPES()
    except AttributeError:
        constants = {}
    return {
        'start': '= {',
        'end': '};',
        'constant_types': constants,
        'languages': settings.LANGUAGES,
    }