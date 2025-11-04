FROM python:3.11-slim

# Instala Java para language_tool_python
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk-headless \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas os arquivos do backend
COPY main.py .
COPY models/ models/
COPY schemas.py .
COPY crud.py .
COPY autenticacao10/ autenticacao10/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

