from django.urls import reverse

from django_webtest import WebTest

from accounts.tests.factories import UserFactory
from directory.tests.factories import OrganisationFactory
from pages.tests.factories import PageFactory
from resources.choices import RESOURCE_APPROVED
from resources.models import Resource

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


class ResourceCreateViewViewTest(WebTest):

    def setUp(self):
        self.user = UserFactory.create(
            approved_organisations=OrganisationFactory.create_batch(size=10)
        )
        self.initial = {
            'title': 'test',
            'abstract': 'abstract',
            'content': 'content',
        }

    def test_view_no_auth(self):
        response = self.app.get(reverse('resources:resource-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_public(self):
        response = self.app.get(reverse('resources:resource-create'), user=self.user)
        organisation = self.user.approved_organisations.all()[0]
        form = response.form
        for name, field in form.fields.items():
            if self.initial.get(name):
                field[0].value = self.initial[name]
        form['is_public'] = True
        form['organisation'] = str(organisation.id)
        response = form.submit()

        resource = Resource.objects.get(title='test')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resource.organisation_id, organisation.id)
        self.assertFalse(resource.privacy.exists())

    def test_not_public(self):
        response = self.app.get(reverse('resources:resource-create'), user=self.user)
        organisation = self.user.approved_organisations.all()[0]
        form = response.form
        for name, field in form.fields.items():
            if self.initial.get(name):
                form[name].value = self.initial[name]
        form['is_public'] = False
        form['organisation'] = str(organisation.id)
        response = form.submit()

        resource = Resource.objects.get(title='test')
        self.assertEqual(resource.privacy.count(), self.user.approved_organisations.count())
