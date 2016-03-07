from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import EmailSent

EmailSent.view = _('View')


class EmailSentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'sent_to',
            'timestamp',
            'template',
            'content',
        )}),
    )

    list_display = ('view', 'sent_to', 'template', 'timestamp')
    search_fields = ('sent_to', 'timestamp', 'template', )
    readonly_fields = 'sent_to', 'timestamp', 'template', 'content',
    ordering = ('-timestamp', )


admin.site.register(EmailSent, EmailSentAdmin)
