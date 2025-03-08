from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("__debug__/", include("debug_toolbar.urls")),  # debug toolbar
    path("accounts/", include("django.contrib.auth.urls")),
    # Set GithHub, OAuth Apps, Authorization callback URL, http://<domain>/oauth/complete/github/
    re_path(r"^oauth/", include("social_django.urls", namespace="social")),
    path("", include("core.urls")),
    path("python/", include("python_problems.urls")),
    path("sql/", include("sql_problems.urls")),
    path("forums/", include("forums.urls")),
]


# Switch to social login if it is configured - Keep for later
try:
    from . import github_settings  # github_settings-dist.py
    social_login = "registration/login_social.html"
    urlpatterns = [path('accounts/login/', LoginView.as_view(template_name=social_login))]\
        + urlpatterns
except:
    pass
