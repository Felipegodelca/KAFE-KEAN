from pathlib import Path
import os

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-kafe-kean-secret-key")


def env_bool(*names, default="0"):
    for name in names:
        value = os.environ.get(name)
        if value is not None:
            return value.lower() in {"1", "true", "yes", "on"}
    return default.lower() in {"1", "true", "yes", "on"}


DEBUG = env_bool("DJANGO_DEBUG", "DEBUG", default="0" if os.environ.get("VERCEL") else "1")
IS_PRODUCTION = not DEBUG

if IS_PRODUCTION and SECRET_KEY == "dev-only-kafe-kean-secret-key":
    raise RuntimeError("DJANGO_SECRET_KEY es obligatoria en producción.")


def env_list(names, default):
    if isinstance(names, str):
        names = [names]
    for name in names:
        value = os.environ.get(name)
        if value:
            return [item.strip() for item in value.split(",") if item.strip()]
    return [item.strip() for item in default.split(",") if item.strip()]


ALLOWED_HOSTS = env_list(
    ["DJANGO_ALLOWED_HOSTS", "ALLOWED_HOSTS"],
    "127.0.0.1,localhost" if DEBUG else "kafekean.com,www.kafekean.com,.vercel.app",
)
CSRF_TRUSTED_ORIGINS = env_list(
    ["DJANGO_CSRF_TRUSTED_ORIGINS", "CSRF_TRUSTED_ORIGINS"],
    "https://kafekean.com,https://www.kafekean.com",
)

vercel_host = os.environ.get("VERCEL_URL") or os.environ.get("VERCEL_BRANCH_URL")
if vercel_host:
    vercel_host = vercel_host.removeprefix("https://").removeprefix("http://").strip("/")
    if vercel_host and vercel_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(vercel_host)
    vercel_origin = f"https://{vercel_host}"
    if vercel_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(vercel_origin)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "articulos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mi_pagina_web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "mi_pagina_web.wsgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL")
if IS_PRODUCTION and not DATABASE_URL:
    raise RuntimeError("DATABASE_URL es obligatoria en producción.")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL or f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=0 if IS_PRODUCTION else 60,
        conn_health_checks=True,
        ssl_require=IS_PRODUCTION,
    )
}

if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    DATABASES["default"]["OPTIONS"].setdefault("connect_timeout", 10)
    # Compatible con el pool de transacciones de Supabase (puerto 6543).
    DATABASES["default"]["OPTIONS"].setdefault("prepare_threshold", None)
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
    ("de", "Deutsch"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        if IS_PRODUCTION
        else "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = IS_PRODUCTION
SESSION_COOKIE_SECURE = IS_PRODUCTION
CSRF_COOKIE_SECURE = IS_PRODUCTION
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_HSTS_SECONDS = 31536000 if IS_PRODUCTION else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = IS_PRODUCTION

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "articulos:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
