from django.conf.urls import url

from .views import ResourceCreateView

app_name = 'resources'
urlpatterns = [
    url(r'^add/$', ResourceCreateView.as_view(), name='resource-create'),
]
