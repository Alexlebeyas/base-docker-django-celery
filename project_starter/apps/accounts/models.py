from django.db import models
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib.auth.models import PermissionsMixin, UserManager as DjangoUserManager
from django.utils.crypto import salted_hmac
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from libs.emails.mixins import EmailMixin
from libs.nixa_fields import fields as nixa_fields


__author__ = 'snake'


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now_ = now()

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser,
            date_joined=now_,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **fields):
        return self._create_user(is_staff=False, is_superuser=False, **fields)

    def create_superuser(self, **fields):
        return self._create_user(is_staff=True, is_superuser=True, **fields)


class AuthUser(PermissionsMixin, models.Model):
    """
    Based class of all users in proprio direct. Names, email and language code added.
    Used for the admin
    """
    email = nixa_fields.EmailField(unique=True)
    password = nixa_fields.PasswordField()
    date_joined = models.DateTimeField(_('date joined'), default=now)
    last_login = models.DateTimeField(_('last login'), default=now)
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.'),
    )

    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        abstract = True

    def __str__(self):
        return self.email

    def natural_key(self):
        return self.get_username()

    def get_username(self):
        """
        Return the identifying username for this User
        """
        return getattr(self, self.USERNAME_FIELD)

    is_anonymous = staticmethod(lambda: False)
    is_authenticated = staticmethod(lambda: True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password_):
            self.set_password(raw_password_)
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    has_usable_password = lambda self: is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Returns an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()


class User(EmailMixin, AuthUser):
    user_type = 'user'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    first_name = nixa_fields.FirstNameField()
    last_name = nixa_fields.LastNameField()

    @property
    def full_name(self):
        return ' '.join((self.first_name, self.last_name))
