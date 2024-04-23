from django.urls import path, include
from django.contrib.auth import views

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index_view, name="index"),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path("login/", views.LoginView.as_view(template_name="core/core_login.html"), name="login-view"),
    path("contact/", views.contact_view, name="contact"),
]

# , authentication_form=LoginForm