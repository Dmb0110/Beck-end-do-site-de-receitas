
'''
from fastapi import APIRouter, Depends,status, Request
from app.schemas.schemas import CriarReceita,ReceitaOut
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.crud_services.receita_auth_post_service import ReceitaService
from app.autenticacao10.jwt_auth2 import verificar_token,corrigir_texto
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests

router = APIRouter()

security = HTTPBearer()

@router.post(
        '/enviar',
        summary='Rota protegida pra criar receita',
        response_model=ReceitaOut,
        status_code=status.HTTP_201_CREATED
)
def enviar(
    criar: CriarReceita,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    username = verificar_token(credentials)
    
    # Corrige texto antes de salvar
    criar.nome_da_receita = corrigir_texto(criar.nome_da_receita)
    criar.ingredientes = corrigir_texto(criar.ingredientes)
    criar.modo_de_preparo = corrigir_texto(criar.modo_de_preparo)

    return ReceitaService.criar_receita_auth(criar,db,username)
'''



from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests

from app.schemas.schemas import CriarReceita, ReceitaOut
from app.database.session import get_db
from app.crud_services.receita_auth_post_service import ReceitaService
from app.autenticacao10.jwt_auth2 import verificar_token, corrigir_texto

router = APIRouter()
security = HTTPBearer()

UNSPLASH_API_KEY = "SUA_CHAVE_AQUI"  # coloque sua chave da API

@router.post(
    "/enviar",
    summary="Rota protegida pra criar receita",
    response_model=ReceitaOut,
    status_code=status.HTTP_201_CREATED,
)
def enviar(
    criar: CriarReceita,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    username = verificar_token(credentials)

    # Corrige texto antes de salvar
    criar.nome_da_receita = corrigir_texto(criar.nome_da_receita)
    criar.ingredientes = corrigir_texto(criar.ingredientes)
    criar.modo_de_preparo = corrigir_texto(criar.modo_de_preparo)

    # 🔎 Busca imagem real do prato
    url = f"https://api.unsplash.com/search/photos?query={criar.nome_da_receita}&client_id={UNSPLASH_API_KEY}"
    response = requests.get(url).json()
    imagem_url = None
    if response.get("results"):
        imagem_url = response["results"][0]["urls"]["regular"]

    # Salva receita no banco
    receita = ReceitaService.criar_receita_auth(criar, db)

    # Adiciona a URL da imagem ao retorno
    receita_dict = receita.__dict__
    receita_dict["imagem_url"] = imagem_url

    return receita_dict


'''
codigo do arquivo index.html do site de receitas:
(essa parte nao gera imagem na pgina web)

    async function carregarReceitas() {
      const container = document.getElementById("lista-receitas");
      container.innerHTML = "";
      const receitas = await buscarReceitas();

      receitas.forEach(r => {
        const div = document.createElement("div");
        div.innerHTML = `
          <div class="titulo-receita" onclick="window.location.href='receita.html?id=${r.id}'">${r.nome_da_receita}</div>
          <div class="detalhes-receita" id="detalhes-${r.id}">
            <strong>Ingredientes:</strong><br> ${formatarIngredientes(r.ingredientes)}<br>
            <strong>Modo de preparo:</strong><br> ${r.modo_de_preparo}
          </div>
        `;
        container.appendChild(div);
      });


      (o trecho abaixo gera imagem)

      
    receitas.forEach(r => {
      const div = document.createElement("div");
      div.innerHTML = `
        <div class="titulo-receita" onclick="window.location.href='receita.html?id=${r.id}'">
          ${r.nome_da_receita}
        </div>
        ${r.imagem_url ? `<img src="${r.imagem_url}" alt="${r.nome_da_receita}" style="max-width:100%;border-radius:8px;margin:10px 0;" />` : ""}
        <div class="detalhes-receita" id="detalhes-${r.id}">
          <strong>Ingredientes:</strong><br> ${formatarIngredientes(r.ingredientes)}<br>
          <strong>Modo de preparo:</strong><br> ${r.modo_de_preparo}
        </div>
      `;
      container.appendChild(div);
      });
'''