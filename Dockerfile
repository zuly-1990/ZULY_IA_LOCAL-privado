FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del proyecto
COPY core/ ./core/
COPY tools/ ./tools/
COPY patterns/ ./patterns/
COPY decision_engine.py .

# Crear directorios necesarios
RUN mkdir -p ZULY_LAB/resultados_zuly \
    ZULY_PROJECTS \
    bitacora/jues_reports \
    memory

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Comando por defecto
CMD ["python", "tools/zuly_qa_runner.py"]
