from django import template
from django.contrib.staticfiles import finders

__author__ = 'nixa'

register = template.Library()


@register.simple_tag
def include_static(path, encoding='UTF-8'):
    file_path = finders.find(path)
    with open(file_path, "r", encoding=encoding) as f:
        string = f.read()
        return string