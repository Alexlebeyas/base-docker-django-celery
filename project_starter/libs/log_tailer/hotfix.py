from os import path
from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape
from .utils import tail_log


def tail_info(request):
    filename = path.join(settings.BASE_DIR, 'logs', 'main.log')
    lines = tail_log(open(filename, 'rb'), lines=100)
    escaped_lines = (escape(line.decode()) for line in lines)
    raw_text = '<br>'.join(escaped_lines)
    return HttpResponse(raw_text)
