# 1. Usar una imagen oficial de Python liviana
FROM python:3.10-slim

# 2. Configurar variables de entorno para Python y Streamlit
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

# 3. Crear y establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar las dependencias primero (aprovecha la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo el código de tu proyecto al contenedor (app.py, reglas.py, etc.)
COPY . .

# 6. Exponer el puerto configurado (8080 es el estándar común en Fury y contenedores web)
EXPOSE 8080

# 7. Comando para ejecutar tu aplicación Streamlit
CMD ["streamlit", "run", "app.py"]
