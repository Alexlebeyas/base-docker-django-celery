from django.conf import settings
from django.db import models
from django.test import SimpleTestCase
from .classes import EmailUser
from .mixins import EmailMixin
from .settings import USER_LANG_FIELD, USER_ACTIVE_FIELD

__author__ = 'snake'


class TestUser(EmailMixin, models.Model):
    email = models.CharField(max_length=256)

    class Meta:
        abstract = True  # no need to query


class EmailUserTest(SimpleTestCase):
    def setUp(self):
        self.test_email = 'someone@test.com'

    def test_user_mixin(self):
        """
        Test functions of EmailUser instantiated with an object subclassing EmailMixin.
        """
        mixin_attributes = {USER_LANG_FIELD: 'fr', USER_ACTIVE_FIELD: False}
        custom_email_user = EmailUser(TestUser(email=self.test_email, **mixin_attributes))

        # Every attributes correspond to their original value.
        self.assertTrue(custom_email_user.get_email() == self.test_email)
        self.assertTrue(custom_email_user.get_lang() == 'fr')
        self.assertTrue(not custom_email_user.is_active())

        default_email_user = EmailUser(TestUser(email=self.test_email))

        # Every attributes used default settings.
        self.assertTrue(default_email_user.get_lang() == settings.LANGUAGE_CODE)
        self.assertTrue(default_email_user.is_active())

    def test_email_string(self):
        """
        Test functions of EmailUser instantiated with an email string.
        """
        email_user = EmailUser(self.test_email)
        self.assertTrue(email_user.get_email() == self.test_email)

        # Every attributes used default settings.
        self.assertTrue(email_user.get_lang() == settings.LANGUAGE_CODE)
        self.assertTrue(email_user.is_active())


class EmailTest(SimpleTestCase):
    pass
    # tODO add if logic to include or exclude email templates from this app to do testing