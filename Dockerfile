FROM python:3.14-slim

# No mostrar actualización de pip y evitar escritura de archivos .pyc
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar e instalar dependencias primero (aprovechando la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#COPIAR ARCHIVOS EN DIRECTORIO LOCAL EN DIRECTORIO DE LA IMAGEN
COPY . .

#EXPOSICION DEL PUERTO DE LA IMAGEN
EXPOSE 8000

#COMANDOS DE EJECUCION DEL APLICATIVO: uvicorn src.main:app --host 0.0.0.0 --port 8085 --reload
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

