from django.conf.urls import url

from .views import PageDetailView

app_name = 'pages'
urlpatterns = [
    url(r'^(?P<url>.*)$', PageDetailView.as_view(), name='page-detail'),
]
