from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

__author__ = 'marcantoine'

class FrontendSitemap(Sitemap):
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)