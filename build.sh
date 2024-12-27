#!/bin/bash

# Mostrar comandos y detener ejecución en caso de errores
set -e

# Actualizar e instalar dependencias de sistema necesarias
apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libzmq3-dev \
    pkg-config \
    gcc \
    g++ \
    python3-pip \
    libffi-dev \
    libssl-dev

# Actualizar pip
pip install --upgrade pip setuptools wheel

# Instalar versiones específicas de dependencias críticas
pip install pyzmq==24.0.1 --no-cache-dir
pip install requests==2.32.3 --no-cache-dir
pip install gunicorn==23.0.0 --no-cache-dir

# Instalar dependencias del proyecto desde requirements.txt
pip install -r requirements.txt --no-cache-dir