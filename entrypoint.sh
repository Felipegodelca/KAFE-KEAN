#!/bin/bash

# Salir si algo falla
set -e

# Aplicar migraciones de base de datos
python manage.py migrate --noinput

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar el servidor
gunicorn mi_pagina_web.wsgi:application --bind 0.0.0.0:8000