"""
ASGI config for mi_pagina_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Establece el módulo de configuración según el entorno (desarrollo o producción)
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_pagina_web.settings.production')  # Configuración para producción
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_pagina_web.settings')  # Configuración para desarrollo

application = get_asgi_application()