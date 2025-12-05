from fastapi import APIRouter, Depends, status
from app.crud_services.receita_crud_service import ReceitaService
from app.schemas.schemas import CriarReceita, ReceitaOut, Atualizar
from typing import List

# Prefixo '/cliente' → todas as rotas começam com /cliente
#router = APIRouter(prefix="/cliente")
router = APIRouter()

@router.get(
    '/health/',
    summary='Verifica status da api',
    status_code=status.HTTP_200_OK
)
def health_check():
    # Endpoint simples de health check, útil para monitoramento e integração com ferramentas de observabilidade.
    return {'Status': 'Ola desenvolvedor,tudo ok por aqui'}


@router.get(
    "/",
    summary="Retorna todas as receitas",
    response_model=List[ReceitaOut],
    status_code=status.HTTP_200_OK
)
def receber(service: ReceitaService = Depends()):
    """
    Lista todos os clientes cadastrados.
    Retorna uma lista de ClienteOut.
    """
    return service.receber_todos_as_receitas()


@router.put(
    "/{receita_id}",
    summary="Trocar dados da receita",
    response_model=ReceitaOut,
    status_code=status.HTTP_200_OK
)
def trocar(
    receita_id: int,
    at: Atualizar,
    service: ReceitaService = Depends()
):
    """
    Atualiza dados de um cliente existente.
    - `cliente_id`: identificador do cliente.
    - `at`: schema com campos opcionais para atualização.
    Retorna o cliente atualizado como ClienteOut.
    """
    return service.trocar_receita(receita_id, at)


@router.delete(
    "/{receita_id}",
    summary="Deletar uma receita",
    status_code=status.HTTP_200_OK
)
def deletar(
    receita_id: int,
    service: ReceitaService = Depends()
):
    """
    Remove um cliente do banco de dados.
    Retorna mensagem de sucesso ou lança 404 se não encontrado.
    """
    return service.deletar_receita(receita_id)
