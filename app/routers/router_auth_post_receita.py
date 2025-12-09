######################################################
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests

from app.schemas.schemas import CriarReceita, ReceitaOut
from app.database.session import get_db
from app.crud_services.receita_auth_post_service import ReceitaService
from app.models.models_receita import Receita
from app.autenticacao10.jwt_auth2 import verificar_token, corrigir_texto

router = APIRouter()
security = HTTPBearer()

# Exemplo: chave de API de um serviço de geração de imagens (OpenAI, Replicate, Stability etc.)
IA_API_KEY = "53619592-285ee82e135be902f1ae2b184"

def gerar_imagem_por_ia(titulo: str,ingredientes: str) -> str | None:
    """
    Gera uma imagem da receita usando IA com base no título.
    Retorna a URL da imagem gerada.
    """

    prompt = (
    f"Fotografia gastronômica profissional de {titulo}. "
    f"Prato típico brasileiro feito com {ingredientes}, "
    f"servido em prato branco, com fundo de mesa de madeira, "
    f"iluminação natural e estilo editorial de revista de culinária."
    )
    '''
    prompt = (
    f"Foto realista de um prato chamado {titulo}. "
    f"Prato típico da culinária brasileira, servido em um prato branco, "
    f"com ingredientes visíveis e iluminação natural de restaurante."
    )
    '''
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",  # ou outro endpoint de IA
            headers={
                "Authorization": f"Bearer {IA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-image-1",   # modelo de geração de imagem
                "prompt": prompt,
                "size": "1024x1024",
                "n": 1
            },
            timeout=30
        )

        if response.status_code != 200:
            print("Erro ao gerar imagem:", response.status_code, response.text)
            return None

        data = response.json()
        # dependendo da API, pode vir como URL direto ou base64
        if "data" in data and data["data"]:
            return data["data"][0].get("url") or None
        return None

    except Exception as e:
        print("Erro ao chamar IA:", e)
        return None


def atualizar_imagens_antigas(db: Session, limite: int = 5) -> int:
    """
    Atualiza automaticamente receitas antigas sem imagem.
    """
    receitas = db.query(Receita).filter(Receita.imagem_url == None).limit(limite).all()
    atualizadas = 0

    for receita in receitas:
        imagem_url = gerar_imagem_por_ia(receita.nome_da_receita)
        if imagem_url:
            receita.imagem_url = imagem_url
            db.add(receita)
            atualizadas += 1

    if atualizadas > 0:
        db.commit()

    return atualizadas


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

    # 🔎 Gera imagem da receita com IA
    imagem_url = gerar_imagem_por_ia(criar.nome_da_receita,ingredientes)

    # Salva receita no banco com imagem
    receita = ReceitaService.criar_receita_auth(criar, db, imagem_url=imagem_url)

    # ⚡ Atualiza automaticamente algumas receitas antigas sem imagem
    atualizar_imagens_antigas(db)

    return receita




######################################################
'''
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests

from app.schemas.schemas import CriarReceita, ReceitaOut
from app.database.session import get_db
from app.crud_services.receita_auth_post_service import ReceitaService
from app.models.models_receita import Receita
from app.autenticacao10.jwt_auth2 import verificar_token, corrigir_texto

router = APIRouter()

security = HTTPBearer()

# 🔑 Sua chave real do Pixabay
PIXABAY_API_KEY = "53619592-285ee82e135be902f1ae2b184"

def buscar_imagem_por_titulo(titulo: str) -> str | None:
    """Consulta a API do Pixabay e retorna a URL da primeira imagem encontrada."""
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={titulo}&image_type=photo&per_page=3"
    try:
        response = requests.get(url, timeout=10)  # timeout evita travar
        if response.status_code != 200:
            print("Erro na requisição:", response.status_code, response.text)
            return None

        data = response.json()  # tenta converter para JSON
        if data.get("hits"):
            return data["hits"][0]["webformatURL"]
        return None
    except Exception as e:
        print("Erro ao buscar imagem:", e)
        return None

'''

'''
def buscar_imagem_por_titulo(titulo: str) -> str | None:
    """Consulta a API do Pixabay e retorna a URL da primeira imagem encontrada."""
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={titulo}&image_type=photo&per_page=1"
    response = requests.get(url).json()
    if response.get("hits"):
        return response["hits"][0]["webformatURL"]
    return None
'''
'''
def atualizar_imagens_antigas(db: Session, limite: int = 5) -> int:
    """
    Atualiza automaticamente receitas antigas sem imagem.
    Por padrão, atualiza até 'limite' receitas por vez para não deixar lento.
    """
    receitas = db.query(Receita).filter(Receita.imagem_url == None).limit(limite).all()
    atualizadas = 0

    for receita in receitas:
        imagem_url = buscar_imagem_por_titulo(receita.nome_da_receita)
        if imagem_url:
            receita.imagem_url = imagem_url
            db.add(receita)
            atualizadas += 1

    if atualizadas > 0:
        db.commit()

    return atualizadas

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

    # 🔎 Busca imagem real do prato pelo título
    imagem_url = buscar_imagem_por_titulo(criar.nome_da_receita)

    # Salva receita no banco com imagem
    receita = ReceitaService.criar_receita_auth(criar, db, imagem_url=imagem_url)

    # ⚡ Atualiza automaticamente algumas receitas antigas sem imagem
    atualizadas = atualizar_imagens_antigas(db)

    return receita
'''


'''
    # Retorno inclui a receita criada e quantas antigas foram atualizadas
    return {
        "nova_receita": receita,
        "receitas_antigas_atualizadas": atualizadas
    }
'''



######################################################


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


##############################################################
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
###########################################################
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

PIXABAY_API_KEY = "53619592-285ee82e135be902f1ae2b184" # coloque sua chave da API

def buscar_imagem_por_titulo(titulo: str) -> str | None:
    """Consulta a API do Pixabay e retorna a URL da primeira imagem encontrada."""
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={titulo}&image_type=photo&per_page=1"
    response = requests.get(url).json()
    if response.get("hits"):
        return response["hits"][0]["webformatURL"]
    return None

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

    # 🔎 Busca imagem real do prato pelo título
    imagem_url = buscar_imagem_por_titulo(criar.nome_da_receita)

    # Salva receita no banco
    receita = ReceitaService.criar_receita_auth(criar, db,imagem_url=imagem_url)

    # Adiciona a URL da imagem ao retorno
    receita_dict = receita.__dict__
    receita_dict["imagem_url"] = imagem_url

    return receita_dict


'''
#############################################################

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