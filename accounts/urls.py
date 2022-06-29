from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, home

app_name = "accounts"

urlpatterns = [
    path("home/", home, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
