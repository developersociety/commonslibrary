from django.conf.urls import url

from comments.views import CommentUpdateView, ReportCommentView
from pages.views import PageDetailView

from .views import (
    ResourceCategoryDetailView, ResourceCreateView, ResourceDetailView, ResourceUpdateView,
    admin_categorise_resources_view
)

app_name = 'resources'
urlpatterns = [
    url(
        r'categorise-resources/$',
        admin_categorise_resources_view,
        name='admin-categorise-resources'
    ),
    url(r'^add/$', ResourceCreateView.as_view(), name='resource-create'),
    url(r'^thank-you/$', PageDetailView.as_view(), name='resource-thank-you'),
    url(
        r'^category/(?P<slug>[\w-]+)/$',
        ResourceCategoryDetailView.as_view(),
        name='resource-category-detail'
    ),
    url(r'^(?P<slug>[\w-]+)/$', ResourceDetailView.as_view(), name='resource-detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', ResourceUpdateView.as_view(), name='resource-update'),
    url(
        r'^(?P<slug>[\w-]+)/(?P<id>[0-9]+)/report-comment/$',
        ReportCommentView.as_view(),
        name='resource-report-comment',
    ),
    url(
        r'^(?P<slug>[\w-]+)/(?P<id>[0-9]+)/update-comment/$',
        CommentUpdateView.as_view(),
        name='resource-update-comment',
    ),
]
