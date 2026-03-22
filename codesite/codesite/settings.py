"""
Django settings for codesite project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = "Codesite"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(rb%k$#$!2p!)_!ob^=zjhj+48mbcxf9rx)i0vo4igx=txwb5r'

# SECURITY WARNING: don't run with debug turned on in production!
# When False encable static files handler
DEBUG = True if os.getenv("DJANGO_DEBUG", "False") == "True" else False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "ukasz.eu.pythonanywhere.com",
    "localhost",  # local Docker
    "codesite.onrender.com",  # Docker container on Render
    ".koyeb.app",  # Allows all subdomains of koyeb.app
    "testserver",  # Testing in Activity Bar
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # "debug_toolbar",  # debug toolbar
    "rest_framework",  # rest framework

    # Extensions - installed with requirements.txt
    'crispy_forms',
    'crispy_bootstrap5',
    'social_django',  # for social login, social-auth-app-django

    # Apps
    "core",
    "python_problems",
    "sql_problems",
    "forums",
    "animations",

]

# When we get to tagging

# When we get to crispy forms :)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

TAGGIT_CASE_INSENSITIVE = True

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",  # Debug Toolbar
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # static files handler
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # social login


]

ROOT_URLCONF = 'codesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.settings',      # Add context_processors.py to core dir
                'social_django.context_processors.backends',  # Social
                'social_django.context_processors.login_redirect',  # Social
            ],
        },
    },
]

WSGI_APPLICATION = 'codesite.wsgi.application'


DATABASES = {
    # sqlite3
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },

    # MySQL on localhost
    'default2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codesite_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },

    # MySQL on pythonanywhere
    'default3': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ukasz$codesite_db',
        'USER': 'ukasz',
        'PASSWORD': 'codesite',
        'HOST': 'ukasz.mysql.eu.pythonanywhere-services.com',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
# for static files "STATIC_ROOT = BASE_DIR / 'static_collected'"
STATIC_ROOT = BASE_DIR / 'staticfiles'
# for global files, The search starts in the directories listed in STATICFILES_DIRS, using the order you have provided. Then, if the file is not found, the search continues in the static folder of each application.
STATICFILES_DIRS = [BASE_DIR / 'mystaticfiles']
# Cache busting. Forces browsers to download the latest version of files (CSS, JavaScript, images).
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"


# Configure the social login
SOCIAL_AUTH_GITHUB_KEY = os.getenv("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

try:
    from . import github_settings
    SOCIAL_AUTH_GITHUB_KEY = SOCIAL_AUTH_GITHUB_KEY or github_settings.SOCIAL_AUTH_GITHUB_KEY
    SOCIAL_AUTH_GITHUB_SECRET = SOCIAL_AUTH_GITHUB_SECRET or github_settings.SOCIAL_AUTH_GITHUB_SECRET
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY or github_settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET or github_settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
    # SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = github_settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI
finally:
    pass


# Social
AUTHENTICATION_BACKENDS = (
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    # "social_core.backends.google_onetap.GoogleOneTap",
    # "social_core.backends.twitter.TwitterOAuth",
    # "social_core.backends.facebook.FacebookOAuth2",

    "django.contrib.auth.backends.ModelBackend",
)


# LOGIN_URL = 'login' # view name
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_URL = 'logout'
# LOGOUT_REDIRECT_URL = 'login'

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
# Don't set default LOGIN_URL - let django.contrib.auth set it when it is loaded
# LOGIN_URL = '/accounts/login'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Debug Toolbar
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]
