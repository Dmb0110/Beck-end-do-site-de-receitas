from fastapi import APIRouter, Depends, status
from app.crud_services.receita_crud_service import ReceitaService
from app.schemas.schemas import CriarReceita, ReceitaOut, Atualizar
from typing import List

# Cria um roteador para agrupar rotas relacionadas a receitas
# Poderia ter um prefixo (ex.: prefix="/receita") para organizar melhor a API
router = APIRouter()

@router.get(
    '/health/',
    summary='Verifica status da API',
    status_code=status.HTTP_200_OK
)
def health_check():
    """
    Endpoint simples de health check.
    Útil para monitoramento e integração com ferramentas de observabilidade.
    Retorna um JSON indicando que a API está funcionando.
    """
    return {'Status': 'Ola desenvolvedor, tudo ok por aqui'}

@router.get(
    "/receber",
    summary="Retorna todas as receitas",
    response_model=List[ReceitaOut],
    status_code=status.HTTP_200_OK
)
def receber(service: ReceitaService = Depends()):
    """
    Lista todas as receitas cadastradas.
    Retorna uma lista de objetos ReceitaOut.
    """
    return service.receber_todos_as_receitas()

@router.get(
    '/especifico/{receita_id}',
    summary='Seleciona uma receita específica',
    response_model=ReceitaOut,
    status_code=status.HTTP_200_OK
)
def exibir(receita_id: int, service: ReceitaService = Depends()):
    """
    Retorna uma receita específica pelo ID.
    Lança 404 se não encontrada.
    """
    return service.exibir_receita_especifica(receita_id)

@router.put(
    "/trocar/{receita_id}",
    summary="Atualizar dados da receita",
    response_model=ReceitaOut,
    status_code=status.HTTP_200_OK
)
def trocar(
    receita_id: int,
    at: Atualizar,
    service: ReceitaService = Depends()
):
    """
    Atualiza dados de uma receita existente.
    - `receita_id`: identificador da receita.
    - `at`: schema com campos opcionais para atualização parcial.
    Retorna a receita atualizada como ReceitaOut.
    """
    return service.trocar_receita(receita_id, at)

@router.delete(
    "/deletar/{receita_id}",
    summary="Deletar uma receita",
    status_code=status.HTTP_200_OK
)
def deletar(
    receita_id: int,
    service: ReceitaService = Depends()
):
    """
    Remove uma receita do banco de dados.
    Retorna mensagem de sucesso ou lança 404 se não encontrada.
    """
    return service.deletar_receita(receita_id)
