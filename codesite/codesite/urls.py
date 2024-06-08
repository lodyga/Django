"""
URL configuration for codesite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login_social.html')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('social_auth/', include('social_django.urls', namespace='social')), # social_auth
    re_path(r'^oauth/', include('social_django.urls', namespace='social')), # same as in GithHub http.............../oauth/complete/github/
    path("", include("core.urls")),
    path("python/", include("python_problems.urls")),
    path("sql/", include("sql_problems.urls")),
    path("forums/", include("forums.urls")),
]


# Switch to social login if it is configured - Keep for later
try:
    from . import github_settings  # github_settings-dist.py
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
                       path(
                           'accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    pass
except:
    pass
