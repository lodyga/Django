from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = "core"

urlpatterns = [
    path("", views.index_view, name="index-view"),
    path("contact/", views.contact_view, name="contact-view"),
    path("signup/", views.signup_view, name="signup-view"),
    path("login/", auth_views.LoginView.as_view(template_name="core/core_login.html", authentication_form=LoginForm), name="login-view")
]
