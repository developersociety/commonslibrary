from django.core.urlresolvers import reverse

from django_webtest import WebTest

from pages.tests.factories import PageFactory


class PageDetailTestView(WebTest):

    def setUp(self):
        self.page = PageFactory.create()

    def test_get_object(self):
        response = self.app.get(reverse('pages:page-detail', kwargs={'url': self.page.url}))
        self.assertEqual(response.status_code, 200)

    def test_middleware(self):
        response = self.app.get(self.page.url)
        self.assertEqual(response.status_code, 200)
