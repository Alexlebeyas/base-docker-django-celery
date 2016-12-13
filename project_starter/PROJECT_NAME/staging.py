from os import path

from django.conf import settings

__author__ = 'snake'

DB_USER = '((DB_USER))'
DB_NAME = '((DB_NAME))'
DB_PASS = '((DB_PASS))'
ALLOWED_HOSTS = None,  # tODO add prod IP here.

DEBUG = False
PROJECT_NAME = path.basename(path.dirname(__file__))
PROJECT_DOMAIN = 'http://192.168.2.253'  # TODO changer l'adresse IP

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': DB_USER,
        'NAME': DB_NAME,
        'PASSWORD': DB_PASS,
        'HOST': 'localhost',
    },
}

CACHES = {
    "default": {
        'BACKEND': 'redis_cache.RedisCache',
        "LOCATION": "redis://localhost:6379/0",
        'TIMEOUT': 300,
        'KEY_PREFIX': 'django-%s-' % PROJECT_NAME,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/', ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.static',
                'django.core.context_processors.media',
                'django.contrib.messages.context_processors.messages',

                # DJANGO-CMS
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ),
            'loaders': (
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.app_directories.Loader',
                    'django.template.loaders.filesystem.Loader',
                )),
            ),
        },
    },
)

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = "staging@bonjourresidences.com"

MIDDLEWARE_CLASSES = (
    # DJANGO-CMS - must be place on top
    'cms.middleware.utils.ApphookReloadMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    # SOLID i18n
    'solid_i18n.middleware.SolidLocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # DJANGO-CMS
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'libs.djangocms_ckeditor_filer.middleware.ThumbnailMiddleware',

    'apps.residences.middlewares.FirstLoginMiddleware',

    'libs.middlewares.UpdateCacheMobileMiddleware',
    'libs.middlewares.MobileDetectionMiddleware',
)
