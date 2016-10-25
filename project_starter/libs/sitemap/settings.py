from django.conf import settings

__author__ = 'snake'


ONE_DAY = 86400
SITEMAP_CACHE_KEY = getattr(settings, 'SITEMAP_KEY', '-'.join(('sitemap-84jgh', settings.SECRET_KEY)))
SITEMAP_CACHE_EXPIRATION = getattr(settings, 'SITEMAP_CACHE_EXPIRATION', ONE_DAY)
SITEMAP_EXTRA_URLS = getattr(settings, 'SITEMAP_EXTRA_URLS', set())
SITEMAP_EXTRA_MODELS = getattr(settings, 'SITEMAP_EXTRA_MODELS', set())
