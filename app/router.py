from fastapi import APIRouter
from app.routers.router_registro import router as registro
from app.routers.router_login import router as login
from app.routers.router_auth_post_receita import router as receita_auth
from app.routers.router_crud_receita import router as receita

api_router = APIRouter()

api_router.include_router(registro,prefix='/registro',tags=['registro'])

api_router.include_router(login,prefix='/login',tags=['login'])

api_router.include_router(receita_auth,prefix='/receita_auth',tags=['receita_auth'])

api_router.include_router(receita,prefix='/receita',tags=['receita'])
