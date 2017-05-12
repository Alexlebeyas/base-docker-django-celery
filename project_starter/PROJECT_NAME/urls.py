import hotfix
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from apps.front.views import error
from django.views.i18n import javascript_catalog
from .sitemaps import sitemaps
from django.views.generic import TemplateView

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('apps.custom_admin', 'apps.front', 'apps.user_profile', )
}

urlpatterns = [
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), {
        'PROJECT_URI': settings.PROJECT_URI
    }),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotfix/', include(hotfix)),
    url(r'^emails/', include('nixaemails.urls')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),
    url(r'^', include('apps.front.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns.append(
        url(r'^error', error, name='error')
    )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)