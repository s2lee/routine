from django.test import TestCase

from accounts.models import CustomUser as User


class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="testuser@abc.com", password="password3^")
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "testuser@abc.com")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_raises_error_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "이메일을 설정해야 합니다."):
            User.objects.create_user(email="", password="password3^")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="super@abc.com", password="password5*"
        )
        self.assertIsInstance(admin_user, User)
        self.assertEqual(admin_user.email, "super@abc.com")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)

    def test_create_superuser_with_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(
                email="super@abc.com", password="password5*", is_staff=False
            )

    def test_create_superuser_with_is_superuser_status(self):
        with self.assertRaisesMessage(
            ValueError, "Superuser must have is_superuser=True."
        ):
            User.objects.create_superuser(
                email="super@abc.com", password="password5*", is_superuser=False
            )
