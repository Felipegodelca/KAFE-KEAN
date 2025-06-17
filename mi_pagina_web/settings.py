import os
from pathlib import Path
import environ
import dj_database_url

# ==========================
# 📁 BASE DIRECTORY
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# 🔑 CARGAR VARIABLES DE ENTORNO
# ==========================
env = environ.Env(DEBUG=(bool, False))

# 📌 Intentamos cargar el `.env.consolidado` si existe
env_file = os.path.join(BASE_DIR, '.env.consolidado')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# ==========================
# 🔒 CONFIGURACIÓN DE SEGURIDAD
# ==========================
SECRET_KEY = env('DJANGO_SECRET_KEY', default='fallback-secret-key')
DEBUG = env.bool("DEBUG", default=False)

# ==========================
# 🌐 HOSTS Y CSRF
# ==========================
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    '127.0.0.1', 'localhost', '192.168.100.11',
    'kafekean.com', 'www.kafekean.com'
])

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[
    "http://127.0.0.1", "http://localhost", "http://192.168.100.11",
    "https://kafekean.com", "https://www.kafekean.com"
])


# ==========================
# 🛠️ CONFIGURACIÓN DE BASE DE DATOS
# ==========================
DATABASES = {
    'default': dj_database_url.config(
        default=env("DATABASE_URL", default="sqlite:///db.sqlite3")
    )
}

# ==========================
# 🔐 SEGURIDAD EN PRODUCCIÓN
# ==========================
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# ==========================
# 🌎 INTERNACIONALIZACIÓN
# ==========================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [('en', 'English'), ('es', 'Español'), ('de', 'Deutsch')]
LOCALE_PATHS = [BASE_DIR / 'locale']

# ==========================
# 🛠️ CONFIGURACIÓN DE PLANTILLAS
# ==========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'articulos/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'articulos.context_processors.agregar_imagen_inspiradora',
            ],
        },
    },
]

# ==========================
# 🗂️ ARCHIVOS ESTÁTICOS Y MEDIA
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# 🚀 APLICACIONES INSTALADAS
# ==========================
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'django.contrib.sites', 'allauth', 'allauth.account', 'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 'articulos'
]

# ==========================
# 🛡️ MIDDLEWARE
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================
# 🔑 AUTENTICACIÓN (django-allauth)
# ==========================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# ==========================
# 🛡️ LOGGING
# ==========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'DEBUG' if DEBUG else 'ERROR'},
}

# ==========================
# 🚀 WHITENOISE (Archivos estáticos)
# ==========================
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==========================
# 🔑 UNSPLASH API CONFIG
# ==========================
UNSPLASH_ACCESS_KEY = env('UNSPLASH_ACCESS_KEY', default='tu_unsplash_access_key_aqui')
UNSPLASH_SECRET_KEY = env('UNSPLASH_SECRET_KEY', default='tu_unsplash_secret_key_aqui')

# ==========================
# 🤖 CONFIGURACIÓN DE OPENROUTER API
# ==========================
OPENROUTER_API_KEY = env("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# ==========================
# 🚀 WSGI
# ==========================
WSGI_APPLICATION = 'mi_pagina_web.wsgi.application'

# ==========================
# 📄 URL ROOT
# ==========================
ROOT_URLCONF = 'mi_pagina_web.urls'

# ==========================
# 🔑 PROVEEDORES SOCIALES
# ==========================
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}
