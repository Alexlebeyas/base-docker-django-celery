import hotfix
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from apps.front.views import error
from libs.sitemap.views import Sitemap

urlpatterns = [
    url(r'^sitemap.xml$', Sitemap.as_view(), name='sitemap'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotfix/', include(hotfix)),
    url(r'^emails/', include('nixaemails.urls')),
    url(r'^', include('apps.front.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns.append(
        url(r'^error', error, name='error')
    )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)