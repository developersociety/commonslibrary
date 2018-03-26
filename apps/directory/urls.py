from django.conf.urls import url

from .views import OrganisationDetailView, OrganisationListView, OrganisationUserView

app_name = 'directory'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', OrganisationDetailView.as_view(), name='organisation-detail'),
    url(r'^$', OrganisationListView.as_view(), name='organisation-list'),
    url(r'^people/(?P<pk>\d+)/$', OrganisationUserView.as_view(), name='organisation-user'),
]
