"""
WSGI config for mi_pagina_web project.

It exposes the WSGI callable as a module-level variable named `application`.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# ==========================
# 🌍 Configurar el Entorno
# ==========================
# Configurar el entorno para desarrollo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_pagina_web.settings')

# ==========================
# 🚀 Aplicación WSGI
# ==========================
application = get_wsgi_application()