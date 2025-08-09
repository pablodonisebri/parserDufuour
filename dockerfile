FROM python:3.11-slim


WORKDIR /app

COPY . .

WORKDIR /app/parserDufuour

RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

