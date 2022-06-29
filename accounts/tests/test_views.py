from django.contrib.auth import SESSION_KEY
from django.test import TestCase

from accounts.models import CustomUser as User


class AccountsViewTest(TestCase):
    def setUp(self):
        self.credentials = {"email": "testuser@abc.com", "password": "password3^"}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post("/accounts/login/", self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_active)
        self.assertEquals(str(response.context["user"]), "testuser@abc.com")
        self.assertIn(SESSION_KEY, self.client.session)

    def test_logout(self):
        response = self.client.post("/accounts/logout/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)
