from django.urls import reverse

import factory
from django_webtest import WebTest

from accounts.models import User
from directory.tests.factories import OrganisationFactory


class UserRegistrationTestView(WebTest):

    def setUp(self):
        self.organisation = OrganisationFactory.create()

    def test_user_registration(self):
        form = self.app.get(reverse('accounts:registration')).form

        email = factory.Faker('email').generate({})
        form['first_name'] = factory.Faker('first_name').generate({})
        form['last_name'] = factory.Faker('last_name').generate({})
        form['email'] = email
        form['password'] = 'test123'
        form['confirm_password'] = 'test123'
        form['organisations'] = self.organisation.id

        response = form.submit()

        user = User.objects.get(email=email)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email=email).exists())
        self.assertFalse(user.is_active)
        # Organisation is always required.
        self.assertTrue(user.organisations.count() > 0)
