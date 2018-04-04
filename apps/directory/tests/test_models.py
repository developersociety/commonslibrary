from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from directory.models import Organisation
from resources.tests.factories import ResourceFactory

from .factories import OrganisationFactory


class OrganisationTestCase(TestCase):

    def setUp(self):
        self.organisation = OrganisationFactory.create()

    def test_get_most_published_this_week_30_days_old(self):
        ResourceFactory.create_batch(
            size=30,
            organisation=self.organisation,
            created_at=timezone.now() - timedelta(days=30),
            is_approved=True,
        )
        organisation = Organisation.get_most_published_this_week()

        self.assertIsNone(organisation)

    def test_get_most_published_this_week(self):
        self.organisation_2 = OrganisationFactory.create()
        ResourceFactory.create_batch(
            size=30,
            organisation=self.organisation,
            is_approved=True,
        )
        ResourceFactory.create_batch(
            size=40,
            organisation=self.organisation_2,
            is_approved=True,
        )
        organisation = Organisation.get_most_published_this_week()

        self.assertEqual(self.organisation_2.id, organisation.id)
