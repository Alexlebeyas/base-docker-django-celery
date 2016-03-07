from django.conf import settings
from django.utils.translation import activate, deactivate

__author__ = 'snake'

try:
    from django.apps import apps
except ImportError:
    # django.db.models.get_models is deprecated since Django 1.7,
    # use django.apps.apps.get_models instead.
    from django.db import models as apps


def get_sitemap_models():
    """
    Iterator for all models subclassing SitemapDisaplayable. Using
    attribute "get_sitemap_queryset" for introspection because
    issubclass is not working in some frameworks (looking at you mezzanine).
    """
    for model in apps.get_models():
        if hasattr(model, 'get_sitemap_queryset'):
            yield model


def get_absolute_urls(models):
    """
    Fetch all urls of each models based on their get_sitemap_queryset() method.
    Models with sitemap_i18n set to True will yield urls in all languages from
    settings.LANGUAGES. Because of i18n's activate/deactivate, must return
    concrete list in case language settings are changed during iteration.
    """
    urls = set()

    def add_urls():
        for o in model.get_sitemap_queryset():
            url = o.get_absolute_url()
            if url:
                urls.add(url)

    for model in models:
        if model.sitemap_i18n:
            for lang, _ in settings.LANGUAGES:
                activate(lang)
                add_urls()
                deactivate()
        else:
            add_urls()
    return urls


class UrlList(object):
    """
    Wrapper for set of urls. Init with url generators
    or lists or add them later with add() method.
    """

    def __init__(self, *url_lists):
        self.urls = set()
        for urls in url_lists:
            self.add(urls)

    def __iter__(self):
        return iter(self.urls)

    def __repr__(self):
        return repr(self.urls)

    def __iadd__(self, other):
        self.add(other)
        return self

    def add(self, urls):
        if urls:
            for url in urls:
                self.urls.add(url)