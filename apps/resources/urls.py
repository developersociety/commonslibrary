from django.conf.urls import url

from .views import ResourceCreateView, ResourceDetailView

app_name = 'resources'
urlpatterns = [
    url(r'^add/$', ResourceCreateView.as_view(), name='resource-create'),
    url(r'^(?P<slug>[\w-]+)/$', ResourceDetailView.as_view(), name='resource-detail'),
]
