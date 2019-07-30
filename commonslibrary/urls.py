from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist, loader

from core.views import ExploreView, HomeView, SearchView

admin.site.site_title = 'Campaigns Library Workspace'
admin.site.site_header = 'Campaigns Library Workspace'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^explore/$', ExploreView.as_view(), name='explore'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^directory/', include('directory.urls')),
    url(r'^resources/', include('resources.urls')),
    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
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
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def handler500(request, template_name='500.html'):
    """ 500 handler with request context. """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    return HttpResponseServerError(template.render({
        'request': request,
    }))
