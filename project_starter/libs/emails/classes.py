from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import TemplateDoesNotExist, Template, Context
from django.template.loader import get_template
from django.utils import translation
from django.utils.translation import get_language
from .exceptions import EmailException
from .loggers import logger
from .models import EmailSent
from .settings import USER_EMAIL_FIELD, USER_LANG_FIELD, USER_ACTIVE_FIELD
from .utils import clean_template_name, prod_cached_property, attach_file_to_email

__author__ = 'snake'


class EmailUser(object):
    """
    Interface object to make abstraction of a recipient's type to normalize
    email address, language and permissions.
    """

    def __init__(self, recipient):
        self.recipient = recipient

    get_email = lambda s: getattr(s.recipient, USER_EMAIL_FIELD, str(s.recipient))
    get_lang = lambda s: getattr(s.recipient, USER_LANG_FIELD, get_language())
    is_active = lambda s: getattr(s.recipient, USER_ACTIVE_FIELD, True)
    __str__ = get_email


class Email(object):
    def __init__(self, template, subject, context, description, reply_to=None):
        self.template = clean_template_name(template)
        self.subject = subject
        self.description = description
        self.reply_to = reply_to
        default_context = self._get_default_context
        full_context = default_context.copy()
        full_context.update(context)
        self.keys = tuple(full_context.keys())
        self.test_values = tuple(full_context.values())

    def __str__(self):
        return self.template

    @prod_cached_property
    def _get_default_context(self):
        return {
            'PROJECT_CONTACT': settings.PROJECT_CONTACT,
            'PROJECT_TITLE': settings.PROJECT_TITLE,
            'PROJECT_DOMAIN': settings.PROJECT_DOMAIN,
            'COLOR_BG_HEADER': getattr(settings, 'COLOR_BG_HEADER', '#6cb33f'),
            'COLOR_BG_FOOTER': getattr(settings, 'COLOR_BG_FOOTER', '#171923'),
            'COLOR_TEXT_HEADER': getattr(settings, 'COLOR_TEXT_HEADER', '#fff'),
            'COLOR_TEXT_FOOTER': getattr(settings, 'COLOR_TEXT_FOOTER', '#fff'),
            'COLOR_TEXT_LINKS': getattr(settings, 'COLOR_TEXT_LINKS', '#6cb33f'),
            'COLOR_BORDER_HEADER': getattr(settings, 'COLOR_TEXT_LINKS', '#6cb33f'),
            'COLOR_BORDER_BODY': getattr(settings, 'COLOR_BORDER_BODY', '#AFB6CC')
        }

    def send(self, recipients, context, lang=None, reply_to=None, commit=True, files=None):
        """
        Send emails to a list of recipients. They can either be email strings or
        objects with email mixin. Context is validated and emails are sent separately.
        The parameters `lang` and `reply_to` are overrides and optional.
        """
        self._validate_context(context)
        context = Context(context)
        for recipient in recipients:
            self._send_single(recipient, context, lang, reply_to, commit, files)

    def _send_single(self, recipient, context, lang=None, reply_to=None, commit=True, files=None):
        """
        Send email to a single recipient, which can be a string or an object with
        email mixin. Recipients with attribute USER_ACTIVE_FIELD set to False will
        be ignored. If parameter USER_LANG_FIELD is present, it will override the recipient's
        language setting. Subject, plain template and optionally html template, are
        rendered with the right language. Setting the `reply_to` parameter will override
        the template's default value.

        The email is sent if `commit` is set to True, then it is returned.
        Using commit=False is mostly for testing purposes.
        """
        user = EmailUser(recipient)
        if not user.is_active():
            logger.debug('Not sending email to this person because can_receive_emails is set to False: %s' % user)
        else:
            if lang is None:
                lang = user.get_lang()
            with translation.override(lang):
                subject = Template(self.subject).render(context).strip()
                body = self.template_plain.render(context).strip()
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=(user.get_email(),),

                )
                if self.template_html:
                    email.attach_alternative(self.template_html.render(context).strip(), "text/html")
            if reply_to:
                email.extra_headers['Reply-To'] = reply_to
            elif self.reply_to:
                email.extra_headers['Reply-To'] = self.reply_to
            if files:
                for file in files:
                    attach_file_to_email(email, file)
            if commit:
                EmailSent.objects.create(
                    sent_to=user.get_email(),
                    template=self.template,
                    content=body,
                )
            email.send()

            return email

    def _validate_context(self, context):
        """
        Make sure that all the required keys are present to render
        the templates. Raise EmailException if one is missing.
        """
        context_keys = tuple(context.keys())
        for key in filter(lambda k: k not in context_keys, self.keys):
            raise EmailException('Missing key "%s" in context of email template "%s". Required keys are: "%s"'
                                 % (key, self.template, ', '.join(self.keys)))

    @prod_cached_property
    def template_plain(self):
        """
        Plain template loader.
        """
        return get_template('email_templates/plain/%s' % self.template)

    @prod_cached_property
    def template_html(self):
        """
        Html template loader, which is optionnal.
        """
        try:
            return get_template('email_templates/html/%s' % self.template)
        except TemplateDoesNotExist:
            pass

    @prod_cached_property
    def test_context(self):
        """
        Zip the context keys and the test values and serve them as dict.
        """
        return dict(zip(self.keys, self.test_values))

    def render_test_plain(self):
        """
        Plain template renderer. Used for testing.
        """
        return self.template_plain.render(self.test_context).strip()

    def render_test_html(self):
        """
        Html template renderer, might return an empty string. Used for testing.
        """
        if self.template_html:
            return self.template_html.render(self.test_context).strip()
        else:
            return ''

    def get_absolute_url(self):
        return reverse('email_template_single', kwargs={'pk': self.template})
