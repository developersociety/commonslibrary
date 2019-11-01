from django.urls import reverse

from django_webtest import WebTest


class HomeViewTest(WebTest):

    def test_return_code(self):
        response = self.app.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class SearchViewTest(WebTest):

    def test_return_code(self):
        response = self.app.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
