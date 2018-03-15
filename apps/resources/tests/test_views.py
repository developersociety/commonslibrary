from django.urls import reverse

from django_webtest import WebTest

from accounts.tests.factories import UserFactory


class UserDetailTestView(WebTest):

    def setUp(self):
        self.superuser = UserFactory.create(is_superuser=True)

    def test_view_no_auth(self):
        response = self.app.get(reverse('accounts:user-detail'))
        self.assertEqual(response.status_code, 302)

    def test_view(self):
        response = self.app.get(reverse('accounts:user-detail'), user=self.superuser)
        self.assertEqual(response.status_code, 200)
