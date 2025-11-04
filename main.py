
'''
from fastapi import FastAPI
from models.models import Base,engine
from crud import router as crud_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from autenticacao10.jwt_auth2 import router as jwt_router

app = FastAPI()

# Middleware para permitir requisições de outras origens (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode restringir para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas no banco  de dados
Base.metadata.create_all(bind=engine)

# Rotas principais da API
app.include_router(crud_router)
app.include_router(jwt_router)

# Servir arquivos estáticos no frontend
app.mount('/',StaticFiles(directory='front3',html=True), name='static')


'''



from fastapi import FastAPI
from models.models import Base, engine
from crud import router as crud_router
from fastapi.middleware.cors import CORSMiddleware
from autenticacao10.jwt_auth2 import router as jwt_router

app = FastAPI()

# Middleware para permitir requisições do frontend hospedado na Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://receitasmasterchef.vercel.app"],  # Substitua pela URL real do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Rotas principais da API
app.include_router(crud_router)
app.include_router(jwt_router)


'''


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






services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: 'postgresql://neondb_owner:npg_HDj9psUF4Scv@ep-red-meadow-acf8hr0w-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'




 Exemplo de chamada
fetch("https://meu-back.vercel.app/api/login", {
  method: "POST",
  body: JSON.stringify({ email, senha }),
  headers: { "Content-Type": "application/json" }
})




services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: davi9090
      POSTGRES_DB: banco_dmb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:  # renomeado de "web" para "backend" para refletir melhor o propósito
    build: .
    depends_on:
      - db
    ports:
      - "8000:8000"  # ajuste conforme a porta usada pela sua API
    environment:
      DATABASE_URL: postgresql://postgres:davi9090@db:5432/banco_dmb

volumes:
  pgdata:





services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: davi9090
      POSTGRES_DB: banco_dmb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  web:
    build: .
    depends_on:
      - db
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:davi9090@db:5432/banco_dmb

volumes:
  pgdata:




  



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



'''



