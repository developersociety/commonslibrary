from django.conf.urls import url

from .views import OrganisationDetailView, OrganisationListView

app_name = 'directory'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', OrganisationDetailView.as_view(), name='organisation-detail'),
    url(r'^$', OrganisationListView.as_view(), name='organisation-list'),
]
