from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase

from accounts.admin import UserAdmin
from accounts.models import User
from directory.tests.factories import OrganisationFactory

from .factories import UserFactory


class UserAdminTest(TestCase):

    def setUp(self):
        self.user_admin = UserAdmin(User, AdminSite())
        self.superuser = UserFactory.create(is_superuser=True)

        self.organisation = OrganisationFactory.create()
        self.user_with_org = UserFactory.create(is_staff=True)
        self.user_with_org.organisations.add(self.organisation)

        self.user_with_org_1 = UserFactory.create(is_staff=True)
        self.user_with_org_1.organisations.add(self.organisation)

    def test_permissions_with_no_organisation(self):
        self.user_admin.add_remove_permissions(self.superuser)
        self.assertFalse(self.superuser.user_permissions.exists())

    def test_permissions_with_organisation(self):
        self.user_admin.add_remove_permissions(self.user_with_org)
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(content_type=content_type, codename='change_user')
        permission_string = '{app_label}.{permission}'.format(
            app_label=permission.content_type.app_label,
            permission=permission.codename,
        )

        self.assertTrue(self.user_with_org.user_permissions.exists())
        self.assertTrue(self.user_with_org.has_perm(permission_string))

    def test_permissions_delete_organisation(self):
        self.user_with_org.organisations.remove(self.organisation)
        self.user_admin.add_remove_permissions(self.user_with_org)

        self.assertFalse(self.user_with_org.user_permissions.exists())

    def test_get_queryset(self):
        request = RequestFactory().request()
        request.user = self.user_with_org
        qs = self.user_admin.get_queryset(request)

        self.assertEqual(qs.count(), 2)
