from django.db import models

__author__ = 'snake'


class SitemapDisplayable(models.Model):
    sitemap_i18n = False

    class Meta:
        abstract = True

    def get_absolute_url(self):
        raise NotImplementedError('Method "get_absolute_url()" is required by SitemapDisplayable.')

    @classmethod
    def get_sitemap_queryset(cls):
        return cls.objects.all()
