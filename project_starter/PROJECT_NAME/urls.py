import hotfix
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from libs.sitemap import Sitemap

urlpatterns = [
    url(r'^sitemap.xml$', Sitemap.as_view(), name='sitemap'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotfix/', include(hotfix)),
    url(r'^', include('apps.front.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)