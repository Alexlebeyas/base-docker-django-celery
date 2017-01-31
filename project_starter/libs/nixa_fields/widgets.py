import json
from copy import copy
from django import forms as django_forms
from django.forms.utils import flatatt
from django.forms.widgets import DateTimeBaseInput
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.encoding import force_text
from django.utils.html import conditional_escape

from libs.nixa_fields.constants import TimeFormatMap


class MaskWidget(django_forms.TextInput):
    template = "nixa_fields/widget_mask.html"

    def __init__(self, attrs=None):
        if attrs is not None:
            self.input_type = attrs.pop('type', self.input_type)
        super(MaskWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        context = copy(self.attrs)
        if attrs:
            context.update(attrs)

        if attrs.get('class'):
            context['class'] = "%s nixa-fields-mask" % attrs.get('class')
        else:
            context['class'] = "nixa-fields-mask"

        context['vendor_url'] = static('js/jquery.mask.min.js')

        context['name'] = name
        context['value'] = value
        context['input_type'] = self.input_type

        if attrs.get('size'):
            context['size'] = attrs.get('size')

        if attrs.get('max_length'):
            context['max_length'] = attrs.get('max_length')

        return get_template(self.template).render(context)

    class Media:
        js = ('js/mask_widget.js',)


class CCExpirationWidget(django_forms.MultiWidget):
    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]
