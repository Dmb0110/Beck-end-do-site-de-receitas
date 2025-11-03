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









from fastapi import FastAPI
from models.models import Base, engine
from crud import router as crud_router
from fastapi.middleware.cors import CORSMiddleware
from autenticacao10.jwt_auth2 import router as jwt_router

app = FastAPI()

# Middleware para permitir requisições do frontend hospedado na Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meu-front.vercel.app"],  # Substitua pela URL real do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Rotas principais da API
app.include_router(crud_router)
app.include_router(jwt_router)





// Exemplo de chamada
fetch("https://meu-back.vercel.app/api/login", {
  method: "POST",
  body: JSON.stringify({ email, senha }),
  headers: { "Content-Type": "application/json" }
})
