import os
from decouple import config  # Asegúrate de que esté instalado con `pip install python-decouple`
from pathlib import Path
from dotenv import load_dotenv  # Asegúrate de importar load_dotenv
import dj_database_url
import environ

# Inicializar environ
env = environ.Env()

# Leer el archivo .env.consolidado
environ.Env.read_env(os.path.join(BASE_DIR, '.env.consolidado'))

# Determinar el entorno (development o production)
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development').lower()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# Cargar las variables de entorno (usamos python-decouple para gestionarlas)
# ===========================
load_dotenv(dotenv_path=BASE_DIR / '.env.consolidado')  # Cargar el archivo .env que contiene las configuraciones para ambos entornos
print("Dotenv loaded:", os.getenv('DATABASE_URL'))  # Esto debería imprimir la URL de la base de datos si se carga correctamente

# ===========================
# Configuración de seguridad
# ===========================
SECRET_KEY = config('DJANGO_SECRET_KEY', default='fallback-secret-key')

# Usamos una lógica para que se cargue la clave secreta correspondiente según el entorno
DJANGO_SECRET_KEY = config('DJANGO_SECRET_KEY_DEV') if DJANGO_ENV == 'development' else config('DJANGO_SECRET_KEY_PROD')

# Imprimir la clave secreta para verificar que está bien cargada (solo en desarrollo)
if DJANGO_ENV == 'development':
    print("SECRET_KEY:", SECRET_KEY)

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# ===========================
# Configuración de la Base de Datos
# ===========================
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', cast=str)
    )
}

# ===========================
# Configuración de Correo Electrónico
# ===========================
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.office365.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# ===========================
# Seguridad de Cookies y CSRF
# ===========================
SESSION_COOKIE_SECURE = DJANGO_ENV == 'production'
CSRF_COOKIE_SECURE = DJANGO_ENV == 'production'

# ===========================
# Seguridad HSTS (solo en producción)
# ===========================
SECURE_HSTS_SECONDS = 31536000 if DJANGO_ENV == 'production' else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = DJANGO_ENV == 'production'
SECURE_HSTS_PRELOAD = DJANGO_ENV == 'production'
SECURE_SSL_REDIRECT = DJANGO_ENV == 'production'

# ===========================
# Otras configuraciones
# ===========================
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://127.0.0.1,http://localhost').split(',')

# ===========================
# Configuración de Archivos Estáticos
# ===========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ===========================
# Configuración de Archivos de Medios
# ===========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===========================
# Aplicaciones Instaladas
# ===========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',  # Funcionalidades específicas de PostgreSQL
    'articulos',  # Tu aplicación personalizada
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mi_pagina_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Directorio para plantillas personalizadas
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

# ===========================
# Validación de Contraseñas
# ===========================
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

# ===========================
# Internacionalización
# ===========================
LANGUAGE_CODE = 'es'  # Idioma en español
TIME_ZONE = 'America/Mexico_City'  # Zona horaria de México
USE_I18N = True
USE_L10N = True
USE_TZ = True