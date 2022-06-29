from django.core.exceptions import ValidationError


class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            msg = f"비밀번호는 {self.min_length}글자 이상이어야 합니다."
            raise ValidationError(msg, code="password_too_short")

    def get_help_text(self):
        return f"비밀번호는 {self.min_length}글자 이상이어야 합니다."


class ContainsDigitsValidator:
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if sum(c.isdigit() for c in password) < self.min_digits:
            msg = f"현재 비밀번호는 {self.min_digits}개의 숫자를 포함하고 있지 않습니다."
            raise ValidationError(msg, code="password_contains_digits")

    def get_help_text(self):
        return f"비밀번호는 적어도 {self.min_digits}개의 숫자를 포함해야 합니다."


class ContainsSpecialCharactersValidator:
    def __init__(self, min_characters=1):
        self.min_characters = min_characters
        self.characters = set(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")

    def validate(self, password, user=None):
        if sum(c in self.characters for c in password) < self.min_characters:
            msg = f"현재 비밀번호는 {self.min_characters}개의 특수문자를 포함하고 있지 않습니다."
            raise ValidationError(msg, code="password_contains_special_characters")

    def get_help_text(self):
        return f"비밀번호는 적어도 {self.min_characters}개의 특수문자를 포함해야 합니다."
