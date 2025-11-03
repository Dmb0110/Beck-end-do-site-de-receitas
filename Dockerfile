FROM python:3.11-slim

# Instala dependências do sistema, incluindo Java
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk-headless \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY front3/ front3/
COPY main.py .
COPY models.py models.py
COPY schemas.py schemas.py
COPY crud.py crud.py
COPY autenticacao10/ autenticacao10/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
