from django.test import TestCase

from accounts.forms import UserRegistrationForm
from directory.tests.factories import OrganisationFactory


class UserRegistrationFormTest(TestCase):

    def setUp(self):
        self.organisation = OrganisationFactory.create()

    def test_permissions_grant(self):
        """
        Test grant permission to make sure user get's active if email domain matches organisation.
        """
        domain = self.organisation.get_email_domain()

        form = UserRegistrationForm({
            'email': 'test@{}'.format(domain),
            'password': 'test123',
            'confirm_password': 'test123',
            'first_name': 'test',
            'last_name': 'test',
            'chosen_organisations': [self.organisation],
            'privacy_agreement': True,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.approved_organisations.first().id, self.organisation.id)

    def test_permissions_multiple_grants(self):
        """Test orgs are approved if there are multiple matches to the email domain."""

        organisation_a = OrganisationFactory.create(email="test_org_a@test.com")
        organisation_b = OrganisationFactory.create(email="test_org_b@test.com")
        organisation_c = OrganisationFactory.create(email="test_org_c@something.com")

        form = UserRegistrationForm({
            'email': 'test@test.com',
            'password': 'test123',
            'confirm_password': 'test123',
            'first_name': 'test',
            'last_name': 'test',
            'chosen_organisations': [organisation_a, organisation_b],
            'privacy_agreement': True,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIn(organisation_a, user.approved_organisations.all())
        self.assertIn(organisation_b, user.approved_organisations.all())
        self.assertNotIn(organisation_c, user.approved_organisations.all())

    def test_permissions_no_org(self):
        form = UserRegistrationForm({
            'email': 'test@nomatchingdomain.com',
            'password': 'test123',
            'confirm_password': 'test123',
            'first_name': 'test',
            'last_name': 'test',
            'chosen_organisations': [self.organisation],
            'privacy_agreement': True,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.approved_organisations.all().count(), 0)

    def test_permissions_no_grant(self):
        """
        Test grant permission to make sure user get's active if email domain matches organisation.
        """

        form = UserRegistrationForm({
            'email': 'test@nightmare.com',
            'password': 'test123',
            'confirm_password': 'test123',
            'first_name': 'test',
            'last_name': 'test',
            'chosen_organisations': [self.organisation],
            'privacy_agreement': True,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertFalse(user.approved_organisations.exists())
