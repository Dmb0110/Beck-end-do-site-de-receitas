from fastapi import APIRouter
from app.routers.router_registro import router as registro
from app.routers.router_login import router as login
from app.routers.router_auth_post_receita import router as receita_auth
from app.routers.router_crud_receita import router as receita

# Cria um roteador principal que servirá como ponto central para incluir todos os sub-routers da aplicação.
api_router = APIRouter()

# Inclui as rotas de registro de usuários.
# - prefix: define o caminho base da rota (/registro)
# - tags: organiza a documentação no Swagger, agrupando endpoints relacionados
api_router.include_router(registro, prefix='/registro', tags=['registro'])

# Inclui as rotas de login de usuários.
# - prefix: caminho base (/login)
# - tags: facilita a visualização no Swagger
api_router.include_router(login, prefix='/login', tags=['login'])

# Inclui rotas protegidas relacionadas à criação de receitas (necessitam autenticação).
# - prefix: caminho base (/receita_auth)
# - tags: separa endpoints que exigem token JWT
api_router.include_router(receita_auth, prefix='/receita_auth', tags=['receita_auth'])

# Inclui rotas CRUD (Create, Read, Update, Delete) para receitas.
# - prefix: caminho base (/receita)
# - tags: agrupa endpoints de manipulação de receitas
api_router.include_router(receita, prefix='/receita', tags=['receita'])
