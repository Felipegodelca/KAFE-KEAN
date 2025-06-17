# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Da permisos de ejecución al entrypoint
RUN chmod +x /app/entrypoint.sh

# Expone el puerto 8000 (el que usa gunicorn por defecto)
EXPOSE 8000

# Usa el script de entrada
ENTRYPOINT ["/app/entrypoint.sh"]