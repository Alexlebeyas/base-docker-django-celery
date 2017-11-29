# coding: UTF-8
from os import path
import os

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'web', 'localhost']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # SITE-PACKAGE
    'debug_toolbar',
    'crispy_forms',

    # LIBS
    'libs.startup',

    # Nixa libs
    'nixa_emails',
    'nixa_users',

    # APPS
    'apps.front',
)

ADMINS = (
    ('Nixa', 'errors@nixa.ca'),
)

PROJECT_PROTOCOL = '//'
PROJECT_DOMAIN = '127.0.0.1:8000'
PROJECT_URI = "".join((PROJECT_PROTOCOL, PROJECT_DOMAIN))
PROJECT_TITLE = "PROJECT_NAME"
PROJECT_CONTACT = "contact@nixa.com"
PROJECT_SETTINGS = path.dirname(__file__)
BASE_DIR = path.dirname(PROJECT_SETTINGS)
PROJECT_NAME = path.basename(PROJECT_SETTINGS)
SITE_ID = 1

DEBUG = True

LANGUAGE_CODE = "fr"
LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
)

TIME_ZONE = 'US/Eastern'
USE_I18N = True
USE_L10N = True
USE_TZ = True

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

ROOT_URLCONF = '%s.urls' % PROJECT_NAME
STATIC_URL = '/static/'
STATIC_ROOT = path.normpath(path.join(BASE_DIR, 'static'))
MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media')
FIXTURE_DIRS = 'fixtures/',
LOCALE_PATHS = 'locale/',
CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'db',
        'PORT': '5432',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ('templates/',),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": "redis://redis:6379/0",
        'TIMEOUT': 300,
        'KEY_PREFIX': 'django-%s-' % PROJECT_NAME,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
    },
    'formatters': {
        'simple': {'format': '[%(asctime)s] %(levelname)s: %(message)s'},
        'exhaustive': {'format': '[%(asctime)s] %(pathname)s (L: %(lineno)d); %(levelname)s: %(message)s'},
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null', ],
            'propagate': False,
        },
        'main': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console', 'main_file', 'mail_admins', ],
        },
        'django.request': {
            'level': 'ERROR',
            'propagate': True,
            'handlers': ['main_file', 'mail_admins', ],
        },
        'celery': {
            'level': 'INFO',
            'propagate': True,
            'handlers': ['console', 'mail_admins', ],
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false', ],
        },
        'main_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/main.log',
            'maxBytes': 1024 * 1024 * 2,
            'backupCount': 2,
            'formatter': 'simple',
        },
    },
}

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = 'console@localhost'
COLOR_BG_HEADER = '#6cb33f'
COLOR_BG_FOOTER = '#171923'
COLOR_TEXT_HEADER = '#fff'
COLOR_TEXT_FOOTER = '#fff'
COLOR_TEXT_LINKS = '#6cb33f'
COLOR_BORDER_HEADER = '#6cb33f'
COLOR_BORDER_BODY = '#AFB6CC'
################


BROKER_URL = 'redis://localhost:6379/1'
CELERYD_HIJACK_ROOT_LOGGER = False

show_toolbar = lambda r: False

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": '%s.settings.show_toolbar' % PROJECT_NAME,
}

###############################################################################################
# Project specific  #
######################


CKEDITOR_CONFIGS = {
    'default': {
        'enterMode': 2,
        'shiftEnterMode': 1,
        'forcePasteAsPlainText': True,
        'height': 400,
        'width': 500,
        'toolbar': 'Custom',
        'format_tags':'p;h2;h3;h4',
        'toolbar_Custom': [
            ['Source', 'Save'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', 'Undo', 'Redo'],
            ['Find', 'Replace', 'SelectAll'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Format'],
            ['Maximize'],
        ]
    },
    'front': {
        'enterMode': 2,
        'shiftEnterMode': 1,
        'forcePasteAsPlainText': True,
        'height': 400,
        'width': 500,
        'toolbar': 'Custom',
        'format_tags':'p;h2;h3;h4',
        'toolbar_Custom': [
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', 'Undo', 'Redo'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Format'],
        ]
    },
    'client': {
        'enterMode': 2,
        'shiftEnterMode': 1,
        'forcePasteAsPlainText': True,
        'height': 400,
        'width': 500,
        'toolbar': 'Custom',
        'format_tags':'p;h2;h3;h4',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['Format'],
        ]
    }
}

SECRET_KEY = ''
AUTH_USER_MODEL = 'nixa_users.NixaUser'
STARTUP_INITIAL_FIXTURES = ['apps/user_profile/fixtures/admin_user.json']

try:
    from .local_settings import *
except ImportError as e:
    if 'local_settings' not in str(e):
        raise
