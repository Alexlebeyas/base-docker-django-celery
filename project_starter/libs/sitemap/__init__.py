default_app_config = 'libs.sitemap.apps.SiteMapConfig'

__author__ = 'snake'
__version__ = '1.0.0'

# Usage:
#  >> url(r'^sitemap.xml$', Sitemap.as_view(), name='sitemap'),
#
# Add more urls with a list:
#  >> url(r'^sitemap.xml$', Sitemap.as_view(extra_urls=iterable_of_my_urls), name='sitemap'),