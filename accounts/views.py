from django.contrib.auth import login as django_login
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import LoginForm


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = "/accounts/home"

    @method_decorator(sensitive_post_parameters("password"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        django_login(self.request, form.get_user())
        return super().form_valid(form)


def home(request):
    return render(request, "home.html")
