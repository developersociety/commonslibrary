from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase

from accounts.admin import UserAdmin
from accounts.models import User
from directory.tests.factories import OrganisationFactory
from resources.admin import ResourceAdmin
from resources.models import Resource
from resources.tests.factories import ResourceFactory

from .factories import UserFactory


class ResourceAdminTest(TestCase):

    def setUp(self):
        self.resource_admin = ResourceAdmin(Resource, AdminSite())
        self.user_admin = UserAdmin(User, AdminSite())

        self.organisation = OrganisationFactory.create()
        self.resource = ResourceFactory.create(organisation=self.organisation)
        self.resource_1 = ResourceFactory.create(organisation=self.organisation)
        self.resource_2 = ResourceFactory.create()

        self.user_without_organisation = UserFactory.create(is_staff=True)

        self.user_with_organisation = UserFactory.create(is_staff=True)
        self.user_with_organisation.approved_organisations.add(self.organisation)

    def test_permissions_with_no_organisation(self):
        self.user_admin.add_remove_permissions(
            self.user_without_organisation, Resource, 'change_resource'
        )
        self.assertFalse(self.user_without_organisation.user_permissions.exists())

    def test_permissions_with_organisation(self):
        self.user_admin.add_remove_permissions(
            self.user_with_organisation, Resource, 'change_resource'
        )
        content_type = ContentType.objects.get_for_model(Resource)
        permission = Permission.objects.get(content_type=content_type, codename='change_resource')
        permission_string = '{app_label}.{permission}'.format(
            app_label=permission.content_type.app_label,
            permission=permission.codename,
        )

        self.assertTrue(self.user_with_organisation.user_permissions.exists())
        self.assertTrue(self.user_with_organisation.has_perm(permission_string))

    def test_get_queryset(self):
        request = RequestFactory().request()
        request.user = self.user_with_organisation
        qs = self.resource_admin.get_queryset(request)

        self.assertEqual(qs.count(), 2)
