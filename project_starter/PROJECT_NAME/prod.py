from os import path

__author__ = 'snake'

DB_USER = '((DB_USER))'
DB_NAME = '((DB_NAME))'
DB_PASS = '((DB_PASS))'
ALLOWED_HOSTS = None,  # tODO add prod IP here.

DEBUG = False
PROJECT_NAME = path.basename(path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
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
        'DIRS': ('templates/', ),
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.static',
                'django.core.context_processors.media',
                'django.contrib.messages.context_processors.messages',
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
