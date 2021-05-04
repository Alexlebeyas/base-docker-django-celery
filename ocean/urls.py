from django.conf import settings
#from django.conf.urls import include, url
from django.urls import path,include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from apps.front.views import error
#from django.views.i18n import javascript_catalog
from django.views.i18n import JavaScriptCatalog
from .sitemaps import sitemaps
from django.views.generic import TemplateView

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('apps.custom_admin', 'apps.front', 'apps.user_profile',)
}

urlpatterns = [
    path('robots\.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), {'PROJECT_URI': settings.PROJECT_URI}),
    path('sitemap\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('jsi18n', JavaScriptCatalog, js_info_dict, name='javascript-catalog'),
    path('', include('django.contrib.auth.urls')),
    path('', include('apps.front.urls')),

    #url(r'^emails/', include('nixa_emails.urls')),
    #url(r'^', include('nixa_users.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    # urlpatterns.append(path('admin/', admin.site.urls),)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']