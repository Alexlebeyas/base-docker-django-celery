from django.core.cache import cache
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.generic import TemplateView
from .utils import get_sitemap_models, get_absolute_urls, UrlList
from .settings import SITEMAP_CACHE_KEY, SITEMAP_CACHE_EXPIRATION, SITEMAP_EXTRA_URLS

__author__ = 'snake'


class Sitemap(TemplateView):
    def __init__(self, extra_urls=None, use_cache=True, template='sitemap/sitemap.html', **kwargs):
        super(Sitemap, self).__init__(**kwargs)
        self.extra_urls = extra_urls
        self.use_cache = use_cache  # use_cache=False not yet implemented
        self.template = template

    def get_host(self):
        return 'http%(secure)s://%(domain)s' % {
            'secure': 's' if self.request.is_secure() else '',
            'domain': self.request.get_host(),
        }

    def get_urls(self):
        sitemap_models = get_sitemap_models()
        model_urls = get_absolute_urls(sitemap_models)
        return UrlList(model_urls, self.extra_urls, SITEMAP_EXTRA_URLS)

    def render(self, urls):
        context = Context({'host': self.get_host(), 'urls': urls})
        return get_template(self.template).render(context)

    def get(self, request, *args, **kwargs):
        sitemap = cache.get(SITEMAP_CACHE_KEY)
        if not sitemap:
            urls = self.get_urls()
            sitemap = self.render(urls)
            cache.set(SITEMAP_CACHE_KEY, sitemap, SITEMAP_CACHE_EXPIRATION)
        return HttpResponse(sitemap, content_type="text/xml")
