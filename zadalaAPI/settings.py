"""
Django settings for zadalaAPI project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import datetime
import os

from zadala_config import (
    AWS_SECRET_ACCESS_KEY,
    AWS_SECRET_KEY_ID,
    AWS_SNS_ARN,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_PORT,
    EMAIL_HOST_PROVIDER,
    EMAIL_HOST_USER,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    REDIS_DATABASE,
    ZADALA_SECRET_KEY,
    database,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", ZADALA_SECRET_KEY)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if "ENV" in os.environ and os.environ["ENV"] == "prod" else True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "corsheaders",
    "drf_yasg",
    "products",
    "categories",
    "orders",
    "authentication",
    "rest_framework",
    "django_rq",
    "social_auth",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = "zadalaAPI.urls"
TEMPLATE_ROOT = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_ROOT],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "zadalaAPI.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", database["ENGINE"]),
        "NAME": os.environ.get("DB_NAME", database["NAME"]),
        "USER": os.environ.get("DB_USER", database["USER"]),
        "PASSWORD": os.environ.get("DB_PASS", database["PASSWORD"]),
        "HOST": os.environ.get("DB_HOST", database["HOST"]),
        "PORT": os.environ.get("DB_PORT", database["PORT"]),
    }
}

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_THROTTLE_RATES": {
        "logins": "10/hour",
    },
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
}

# JWT_SECRET_KEY = 'secret'


# Customer user model
AUTH_USER_MODEL = "authentication.User"


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_URL = "/images/"
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST_PROVIDER", EMAIL_HOST_PROVIDER)
EMAIL_PORT = os.environ.get("EMAIL_HOST_PORT", EMAIL_HOST_PORT)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", EMAIL_HOST_PASSWORD)
EMAIL_USE_TLS = True

RQ_QUEUES = {
    "default": {
        "HOST": os.getenv("REDIS_HOST", REDIS_DATABASE["HOST"]),
        "PORT": os.getenv("REDIS_PORT", REDIS_DATABASE["PORT"]),
        "DB": os.getenv("REDIS_DB", REDIS_DATABASE["DB"]),
        "PASSWORD": os.getenv("REDIS_PASSWORD", REDIS_DATABASE["PASSWORD"]),
        "DEFAULT_TIMEOUT": os.getenv("REDIS_TIMEOUT", 360),
    },
    "high": {
        "HOST": os.getenv("REDIS_HOST", REDIS_DATABASE["HOST"]),
        "PORT": os.getenv("REDIS_PORT", REDIS_DATABASE["PORT"]),
        "DB": os.getenv("REDIS_DB", REDIS_DATABASE["DB"]),
        "PASSWORD": os.getenv("REDIS_PASSWORD", REDIS_DATABASE["PASSWORD"]),
        "DEFAULT_TIMEOUT": os.getenv("REDIS_TIMEOUT", 500),
    },
    "low": {
        "HOST": os.getenv("REDIS_HOST", REDIS_DATABASE["HOST"]),
        "PORT": os.getenv("REDIS_PORT", REDIS_DATABASE["PORT"]),
        "DB": os.getenv("REDIS_DB", REDIS_DATABASE["DB"]),
        "PASSWORD": os.getenv("REDIS_PASSWORD", REDIS_DATABASE["PASSWORD"]),
    },
}

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", GOOGLE_CLIENT_ID)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", GOOGLE_CLIENT_SECRET)
AWS_SECRET_KEY_ID = os.environ.get("AWS_SECRET_KEY_ID", AWS_SECRET_KEY_ID)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)
AWS_SNS_ARN = os.environ.get("AWS_SNS_ARN", AWS_SNS_ARN)

# Django 3.2
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-SESSION_COOKIE_SECURE
SESSION_COOKIE_SECURE = (
    True
    if "SESSION_COOKIE_SECURE" in os.environ and os.environ["SESSION_COOKIE_SECURE"]
    else False
)

# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-SECURE_SSL_REDIRECT
SECURE_SSL_REDIRECT = (
    True
    if "SECURE_SSL_REDIRECT" in os.environ and os.environ["SECURE_SSL_REDIRECT"]
    else False
)

# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-CSRF_COOKIE_SECURE
CSRF_COOKIE_SECURE = (
    True
    if "CSRF_COOKIE_SECURE" in os.environ and os.environ["CSRF_COOKIE_SECURE"]
    else False
)
