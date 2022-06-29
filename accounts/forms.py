from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django import forms
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="이메일", max_length=255, error_messages={"invalid": "정확한 이메일 형식으로 입력해 주세요."}
    )

    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                msg = "이메일 또는 비밀번호를 잘못 입력했습니다. 입력하신 내용을 다시 확인해주세요."
                raise forms.ValidationError(msg, code="invalid_login")
            else:
                self.confirm_login_allowed(self.user)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            msg = "이 계정은 비활성 상태입니다."
            raise forms.ValidationError(msg, code="inactive")

    def get_user(self):
        return self.user


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
