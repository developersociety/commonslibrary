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
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.approved_organisations.first().id, self.organisation.id)

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
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertFalse(user.approved_organisations.exists())
