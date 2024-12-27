import os
from pathlib import Path
import environ

# ==========================
# 📁 BASE DIRECTORY
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# 🔑 INICIALIZAR ENVIRON
# ==========================
env = environ.Env(
    DEBUG=(bool, False)  # Por defecto, DEBUG estará en False si no se define en el archivo .env
)

# Leer el archivo .env.consolidado
environ.Env.read_env(os.path.join(BASE_DIR, '.env.consolidado'))

# ==========================
# 🔒 CONFIGURACIÓN DE SEGURIDAD
# ==========================
SECRET_KEY = env('DJANGO_SECRET_KEY', default='fallback-secret-key')

# 🚀 Modo de depuración
DEBUG = env.bool('DEBUG', default=True)  # ⚠️ False en producción

# 🌐 Dominios permitidos
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])  # ⚠️ Ajustar en producción

# ==========================
# 🛠️ CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================
DATABASES = {
    'default': env.db(default='sqlite:///db.sqlite3')  # SQLite por defecto, usar PostgreSQL en producción
}

# ==========================
# 📧 CONFIGURACIÓN DE CORREO ELECTRÓNICO
# ==========================
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.office365.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# ==========================
# 🔐 SEGURIDAD DE COOKIES Y CSRF
# ==========================
# ⚠️ En desarrollo, ambas deben ser False
SESSION_COOKIE_SECURE = DEBUG == False  # ⚠️ Cambiar a True en producción
CSRF_COOKIE_SECURE = DEBUG == False  # ⚠️ Cambiar a True en producción

# ⚠️ Forzar solo HTTP en desarrollo para evitar errores HTTPS
SECURE_SSL_REDIRECT = DEBUG == False  # ⚠️ Cambiar a True en producción

# ==========================
# 🔐 SEGURIDAD HSTS (SOLO EN PRODUCCIÓN)
# ==========================
# ⚠️ Ajusta estas opciones en producción
SECURE_HSTS_SECONDS = 0 if DEBUG else 31536000  # ⚠️ 1 año en producción
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG  # ⚠️ True en producción
SECURE_HSTS_PRELOAD = not DEBUG  # ⚠️ True en producción

# ==========================
# 🛡️ CONFIGURACIÓN DE CSRF Trusted Origins
# ==========================
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[
    'http://127.0.0.1',
    'http://localhost'
])  # ⚠️ Agregar dominios en producción

# ==========================
# 🗂️ CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==========================
# 🖼️ CONFIGURACIÓN DE ARCHIVOS DE MEDIOS
# ==========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# 🚀 APLICACIONES INSTALADAS
# ==========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'articulos',  # Tu aplicación personalizada
]

# ==========================
# 🛡️ MIDDLEWARE
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================
# 🛠️ CONFIGURACIÓN DE URLS Y PLANTILLAS
# ==========================
ROOT_URLCONF = 'mi_pagina_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mi_pagina_web.wsgi.application'

# ==========================
# 🔑 VALIDACIÓN DE CONTRASEÑAS
# ==========================
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

# ==========================
# 🌎 INTERNACIONALIZACIÓN
# ==========================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==========================
# ✅ ARCHIVOS ESTÁTICOS EN PRODUCCIÓN
# ==========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'