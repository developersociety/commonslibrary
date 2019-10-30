from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist, loader
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.static import serve

from core.views import HomeView, SearchView
from resources.views import ResourceCategoryListView

admin.site.site_title = 'The Campaigns Library'
admin.site.site_header = 'The Campaigns Library'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^explore/$', ResourceCategoryListView.as_view(), name='resource-category-list'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^directory/', include('directory.urls')),
    url(r'^resources/', include('resources.urls')),
    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
    ),
]

# Make it easier to see a 404 page under debug
if settings.DEBUG:
    from django.views.defaults import page_not_found

    urlpatterns += [
        url(r'^404/$', page_not_found, {'exception': None}),
    ]

# Only enable debug toolbar if it's an installed app
if apps.is_installed('debug_toolbar'):
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# Serving static/media under debug
urlpatterns += static(settings.STATIC_URL, never_cache(staticfiles_serve))
urlpatterns += static(settings.MEDIA_URL, never_cache(serve), document_root=settings.MEDIA_ROOT)


def handler500(request, template_name='500.html'):
    """ 500 handler with request context. """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    return HttpResponseServerError(template.render({
        'request': request,
    }))
