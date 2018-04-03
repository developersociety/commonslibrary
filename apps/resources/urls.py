from django.conf.urls import url

from pages.views import PageDetailView

from .views import ResourceCreateView, ResourceDetailView

app_name = 'resources'
urlpatterns = [
    url(r'^add/$', ResourceCreateView.as_view(), name='resource-create'),
    url(r'^thank-you/$', PageDetailView.as_view(), name='resource-thank-you'),
    url(r'^(?P<slug>[\w-]+)/$', ResourceDetailView.as_view(), name='resource-detail'),
]
