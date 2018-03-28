from django.test import TestCase

from accounts.tests.factories import UserFactory
from directory.tests.factories import OrganisationFactory
from resources.models import Resource
from resources.tests.factories import ResourceFactory


class ResourceManagerTestCase(TestCase):

    def setUp(self):
        self.organisation = OrganisationFactory.create()
        self.user = UserFactory.create(approved_organisations=[self.organisation])
        ResourceFactory.objects.create(is_approved=True, privacy=self.organisation)

    def test_anonymous_approved_resources(self):
        self.assertEqaul(Resource.objects.approved().count(), 1)
