FROM python:3.11-slim

WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .
COPY setup.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=api.main:app
ENV FLASK_RUN_PORT=5000
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
