from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from directory.models import Organisation
from resources.choices import RESOURCE_APPROVED
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
            status=RESOURCE_APPROVED,
        )
        organisation = Organisation.get_most_published_this_week()

        self.assertIsNone(organisation)

    def test_get_most_published_this_week(self):
        self.organisation_2 = OrganisationFactory.create()
        ResourceFactory.create_batch(
            size=30,
            organisation=self.organisation,
            status=RESOURCE_APPROVED,
        )
        ResourceFactory.create_batch(
            size=40,
            organisation=self.organisation_2,
            status=RESOURCE_APPROVED,
        )
        organisation = Organisation.get_most_published_this_week()

        self.assertEqual(self.organisation_2.id, organisation.id)

    def test_get_short_url(self):
        organisation = OrganisationFactory.create(url='http://www.test.com')
        organisation_1 = OrganisationFactory.create(url='http://home.test.com')
        organisation_2 = OrganisationFactory.create(url='http://test.com')

        self.assertEqual(organisation.get_short_url(), 'test.com')
        self.assertEqual(organisation_1.get_short_url(), 'home.test.com')
        self.assertEqual(organisation_2.get_short_url(), 'test.com')

    def test_get_email_domain(self):
        email = 'testing@gmail.com'
        email_1 = 'test1@test.co.uk'
        organisation_1 = OrganisationFactory(email=email)
        organisation_2 = OrganisationFactory(email=email_1)

        self.assertEqual(organisation_1.get_email_domain(), 'gmail.com')
        self.assertEqual(organisation_2.get_email_domain(), 'test.co.uk')
