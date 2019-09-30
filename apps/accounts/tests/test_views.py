from django.conf import settings
from django.urls import reverse

import factory
from django_webtest import WebTest

from accounts.models import User
from accounts.tests.factories import UserFactory
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
        form['chosen_organisations'] = self.organisation.id
        form['privacy_agreement'] = True,

        response = form.submit()

        user = User.objects.get(email=email)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/accounts/thank-you/')

        self.assertTrue(User.objects.filter(email=email).exists())
        self.assertFalse(user.is_active)
        # Organisation is always required.
        self.assertTrue(user.chosen_organisations.count() > 0)


class UserLoginTestView(WebTest):

    def setUp(self):
        self.user = UserFactory.create(password='test123')

    def test_user_login(self):
        form = self.app.get(reverse('accounts:login')).form
        form['username'] = self.user.email
        form['password'] = 'test123'

        response = form.submit()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)


class UserUpdateTestView(WebTest):

    def setUp(self):
        self.user = UserFactory.create(first_name='test123', password='test123')

    def test_update_view(self):
        form = self.app.get(reverse('accounts:user-update'), user=self.user).form
        form['first_name'] = 'test'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email=self.user.email)
        self.assertEqual(user.first_name, 'test')


class UserDetailTestView(WebTest):

    def setUp(self):
        self.superuser = UserFactory.create(is_superuser=True)

    def test_view_no_auth(self):
        response = self.app.get(reverse('accounts:user-detail'))
        self.assertEqual(response.status_code, 302)

    def test_view(self):
        response = self.app.get(reverse('accounts:user-detail'), user=self.superuser)
        self.assertEqual(response.status_code, 200)
