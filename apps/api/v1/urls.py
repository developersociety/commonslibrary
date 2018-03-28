from django.conf.urls import include, url

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'resources', views.ResourceViewSet, base_name='resource')
router.register(r'organisations', views.OrganisationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
