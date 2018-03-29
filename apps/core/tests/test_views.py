from django.urls import reverse

from django_webtest import WebTest


class ApplicationCreateTestView(WebTest):

    def test_application_create(self):
        response = self.app.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
