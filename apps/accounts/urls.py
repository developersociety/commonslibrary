from django.conf.urls import url

from .views import UserCreateView

urlpatterns = [
    url(r'^registration/$', UserCreateView.as_view(), name='registration'),
]
