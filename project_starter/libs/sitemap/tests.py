from django.test import SimpleTestCase
from libs.sitemap.utils import get_sitemap_models, UrlList

__author__ = 'snake'


class SitemapTest(SimpleTestCase):

    def test_get_sitemap_models(self):
        """
        Smoke test - no error is success
        """
        list(get_sitemap_models())

    def test_urllist(self):
        """
        Smoke test - no error is success
        """
        UrlList(['/'])
