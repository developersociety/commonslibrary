from django_webtest import WebTest

from accounts.tests.factories import UserFactory
from comments.models import Comment
from resources.tests.factories import ResourceFactory


class AddCommentTestView(WebTest):

    def setUp(self):
        self.resource = ResourceFactory.create(is_approved=True)
        self.superuser = UserFactory.create(password='test123')

    def test_post_comment_no_auth(self):
        response = self.app.get(self.resource.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertFalse('form' in response)

    def test_check_if_form_exists(self):
        response = self.app.get(self.resource.get_absolute_url(), user=self.superuser)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response)

    def test_post_method(self):
        form = self.app.get(self.resource.get_absolute_url(), user=self.superuser).form
        form['body'] = 'testing'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(created_by=self.superuser).exists())
