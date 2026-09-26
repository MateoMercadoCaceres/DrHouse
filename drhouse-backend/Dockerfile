FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu aplicación
COPY . .

# Cambia al directorio src y ejecuta desde ahí
WORKDIR /app/src
CMD uvicorn main:app --host 0.0.0.0 --port 1712