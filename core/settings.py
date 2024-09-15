import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "phonenumber_field",
    "apps.user",
    "apps.smakolyk",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_POST"),
    }
}


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "smakolyk:home"
LOGOUT_REDIRECT_URL = "smakolyk:home"
AUTH_USER_MODEL = "user.CustomUser"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# SMTP settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Site management settings
ACCOUNTANT = os.environ.get("ACCOUNTANT", "")
ORDERS_RECEIVER = os.environ.get("ORDERS_RECEIVER", "")

# Celery settings
REDIS_IP = os.environ.get("CELERY_BROKER_IP", "redis")
CELERY_BROKER_URL = f"redis://{REDIS_IP}:6379/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_IP}:6379/0"
CELERY_BEAT_SCHEDULE = {
    "send_orders_task": {
        "task": "apps.smakolyk.tasks.send_orders_task",
        "schedule": crontab(hour=18, minute=0, day_of_week="fri"),
    }
}
