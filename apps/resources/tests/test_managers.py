from django.test import TestCase

from accounts.tests.factories import UserFactory
from directory.tests.factories import OrganisationFactory
from resources.models import Resource
from resources.tests.factories import ResourceFactory


class ResourceManagerTestCase(TestCase):

    def setUp(self):
        self.organisation = OrganisationFactory.create()
        self.organisation_1 = OrganisationFactory.create()
        self.user = UserFactory.create(approved_organisations=[self.organisation])
        self.superuser = UserFactory.create(is_superuser=True)

    def test_anonymours_user_resources(self):
        ResourceFactory.create(privacy=[self.organisation], is_approved=True)
        ResourceFactory.create_batch(size=2, is_approved=True)
        ResourceFactory.create(is_approved=False)
        self.assertEqual(Resource.objects.approved().count(), 2)

    def test_user_resources(self):
        ResourceFactory.create(privacy=[self.organisation, self.organisation_1], is_approved=True)
        ResourceFactory.create(privacy=[self.organisation_1], is_approved=True)
        ResourceFactory.create_batch(size=2, is_approved=True)
        ResourceFactory.create(is_approved=False)
        self.assertEqual(Resource.objects.approved(self.user).count(), 3)

    def test_superuser_resources(self):
        ResourceFactory.create(privacy=[self.organisation, self.organisation_1], is_approved=True)
        ResourceFactory.create(privacy=[self.organisation_1], is_approved=True)
        ResourceFactory.create_batch(size=2, is_approved=True)
        ResourceFactory.create(is_approved=False)

        self.assertEqual(Resource.objects.approved(self.superuser).count(), 4)
