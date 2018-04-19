from django.urls import reverse

from django_webtest import WebTest

from accounts.tests.factories import UserFactory
from pages.tests.factories import PageFactory
from resources.choices import RESOURCE_APPROVED

from .factories import ResourceFactory


class ResourceThankTestView(WebTest):

    def setUp(self):
        PageFactory.create(url='/resources/thank-you/')

    def test_view(self):
        response = self.app.get(reverse('resources:resource-thank-you'))
        self.assertEqual(response.status_code, 200)


class ResourceUpdateTestView(WebTest):

    def setUp(self):
        self.resource = ResourceFactory.create(status=RESOURCE_APPROVED)
        self.user = UserFactory.create()

    def test_view_no_auth(self):
        response = self.app.get(
            reverse('resources:resource-update', kwargs={'slug': self.resource.slug})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_with_auth_random(self):
        response = self.app.get(
            reverse('resources:resource-update', kwargs={'slug': self.resource.slug}),
            user=self.user,
            expect_errors=True,
        )
        self.assertEqual(response.status_code, 403)

    def test_view_with_auth(self):
        response = self.app.get(
            reverse('resources:resource-update', kwargs={'slug': self.resource.slug}),
            user=self.resource.created_by,
        )
        form = response.form
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.fields['title'][0].value, self.resource.title)
