from django.conf.urls import url

from .views import ExploreView

app_name = 'explore'
urlpatterns = [
    url(r'^$', ExploreView.as_view(), name='explore-list'),
]
