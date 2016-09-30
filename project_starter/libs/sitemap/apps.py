from django.apps import AppConfig


class SiteMapConfig(AppConfig):
    name = 'libs.sitemap'
    verbose_name = "Sitemap"

    def ready(self):
        from .models import SitemapDisplayable
        from .views import Sitemap