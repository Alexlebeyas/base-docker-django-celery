from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from libs.emails.classes import Email

__author__ = 'Philippe'


contact_email = Email(
    template='contact_email.html',
    subject=_('Contact form submission - Kiski'),
    description='Send this email to admin when a user fill the contact form on home page',
    context={
        'contact': {
            'name': 'Test',
            'email': 'test@test.com',
            'phone': '525-3443',
            'subject': 'Test subject',
            'message': 'Hi, here\'s a test for djfskdl;f sdkjl;fsd \n'
                       'Nixa dlsf sd;kf  dlkfsd dfksd; fsdfkl;ds f;d \n'
                       'fsd ;ls dsad; dmmem eè; l;lj ds; kfl;sd f;sdlf \n'
                       'fl;sdk fs;d; fjsjfnfkddkkdkdkjf ffkkfdkf fdlfl'
        },
        'PROJECT_CONTACT': settings.PROJECT_CONTACT,
        'PROJECT_TITLE': settings.PROJECT_TITLE,
        'PROJECT_DOMAIN': settings.PROJECT_DOMAIN
    },
)