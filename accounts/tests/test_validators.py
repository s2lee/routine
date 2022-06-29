from accounts.validators import (
    MinimumLengthValidator,
    ContainsDigitsValidator,
    ContainsSpecialCharactersValidator,
)
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase


class MinimumLengthValidatorTest(SimpleTestCase):
    def test_validate(self):
        expected_error = "비밀번호는 %d글자 이상이어야 합니다."
        self.assertIsNone(MinimumLengthValidator().validate("12345678"))
        self.assertIsNone(MinimumLengthValidator(min_length=3).validate("123"))

        with self.assertRaises(ValidationError) as cm:
            MinimumLengthValidator().validate("1234567")
        self.assertEqual(cm.exception.messages, [expected_error % 8])
        self.assertEqual(cm.exception.code, "password_too_short")

        with self.assertRaises(ValidationError) as cm:
            MinimumLengthValidator(min_length=3).validate("12")
        self.assertEqual(cm.exception.messages, [expected_error % 3])

    def test_help_text(self):
        self.assertEqual(
            MinimumLengthValidator().get_help_text(),
            "비밀번호는 8글자 이상이어야 합니다.",
        )


class ContainsDigitsValidatorTest(SimpleTestCase):
    def test_validate(self):
        expected_error = "현재 비밀번호는 %d개의 숫자를 포함하고 있지 않습니다."
        self.assertIsNone(ContainsDigitsValidator().validate("password1"))
        self.assertIsNone(ContainsDigitsValidator(min_digits=2).validate("password12"))

        with self.assertRaises(ValidationError) as cm:
            ContainsDigitsValidator().validate("password")
        self.assertEqual(cm.exception.messages, [expected_error % 1])
        self.assertEqual(cm.exception.code, "password_contains_digits")

        with self.assertRaises(ValidationError) as cm:
            ContainsDigitsValidator(min_digits=2).validate("password1")
        self.assertEqual(cm.exception.messages, [expected_error % 2])

    def test_help_text(self):
        self.assertEqual(
            ContainsDigitsValidator().get_help_text(),
            "비밀번호는 적어도 1개의 숫자를 포함해야 합니다.",
        )


class ContainsSpecialCharactersValidatorTest(SimpleTestCase):
    def test_validate(self):
        expected_error = "현재 비밀번호는 %d개의 특수문자를 포함하고 있지 않습니다."
        self.assertIsNone(ContainsSpecialCharactersValidator().validate("password#"))
        self.assertIsNone(
            ContainsSpecialCharactersValidator(min_characters=2).validate("^password$")
        )

        with self.assertRaises(ValidationError) as cm:
            ContainsSpecialCharactersValidator().validate("password")
        self.assertEqual(cm.exception.messages, [expected_error % 1])
        self.assertEqual(cm.exception.code, "password_contains_special_characters")

        with self.assertRaises(ValidationError) as cm:
            ContainsSpecialCharactersValidator(min_characters=2).validate("password@")
        self.assertEqual(cm.exception.messages, [expected_error % 2])

    def test_help_text(self):
        self.assertEqual(
            ContainsSpecialCharactersValidator().get_help_text(),
            "비밀번호는 적어도 1개의 특수문자를 포함해야 합니다.",
        )
