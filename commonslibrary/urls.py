from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist, loader
from django.views.generic import TemplateView

from core.views import HomeView

admin.site.site_title = 'Commons Library'
admin.site.site_header = 'Commons Library'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^group/', TemplateView.as_view(template_name='group.html')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^directory/', include('directory.urls')),
    url(r'^explore/', include('explore.urls')),
    url(r'^resources/', include('resources.urls')),
    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^test/', TemplateView.as_view(template_name='test.html')),
    url(r'^profile/', TemplateView.as_view(template_name='profile.html')),
    url(r'^resource/', TemplateView.as_view(template_name='resource.html')),
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
