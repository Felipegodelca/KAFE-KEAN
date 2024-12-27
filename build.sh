#!/bin/bash

# Actualizar paquetes y dependencias del sistema necesarias para pyzmq
apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libzmq3-dev \
    pkg-config \
    gcc \
    g++

# Instalar dependencias de Python
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir