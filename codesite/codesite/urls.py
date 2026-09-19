from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("__debug__/", include("debug_toolbar.urls")),  # debug toolbar
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r"^oauth/", include("social_django.urls", namespace="social")),
    path("", include("core.urls")),
    path('accounts/login/', LoginView.as_view(template_name="registration/login.html")),
    path("problems/", include("python_problems.urls")),
    # path("sql/", include("sql_problems.urls")),
    path("forums/", include("forums.urls")),
    path("animations/", include("animations.urls")),
]
