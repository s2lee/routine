from django.test import TestCase, override_settings
from django.forms import ValidationError

from accounts.forms import LoginForm
from accounts.models import CustomUser as User


class LoginFormTest(TestCase):
    def setUp(self):
        self.invalid_email = {"email": "invalid_email@", "password": "password#8"}
        self.invalid_login = {
            "email": "invalid_login@abc.com",
            "password": "password#8",
        }
        self.inactive_user = User.objects.create_user(
            email="inactive_user@abc.com", password="password#8", is_active=False
        )
        self.valid_login_user = User.objects.create_user(
            email="valid_login@abc.com", password="password#8"
        )
        self.valid_login_data = {
            "email": "valid_login@abc.com",
            "password": "password#8",
        }

    def test_invalid_email(self):
        form = LoginForm(None, self.invalid_email)
        self.assertFalse(form.is_valid())
        self.assertIn("정확한 이메일 형식으로 입력해 주세요.", form["email"].errors)

    @override_settings(
        AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"]
    )
    def test_invalid_login(self):
        form = LoginForm(None, self.invalid_login)
        self.assertFalse(form.is_valid())
        error_msg = "이메일 또는 비밀번호를 잘못 입력했습니다. 입력하신 내용을 다시 확인해주세요."
        self.assertIn(error_msg, form.non_field_errors())

    def test_confirm_login_allowed(self):
        with self.assertRaises(ValidationError) as cm:
            LoginForm().confirm_login_allowed(self.inactive_user)
        self.assertEqual(cm.exception.messages, ["이 계정은 비활성 상태입니다."])
        self.assertEqual(cm.exception.code, "inactive")

    def test_valid_logins(self):
        data = self.valid_login_data
        form = LoginForm(None, data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertEqual(form.cleaned_data["email"], data["email"])
        self.assertEqual(form.cleaned_data["password"], data["password"])
        self.assertEqual(form.user, self.valid_login_user)
