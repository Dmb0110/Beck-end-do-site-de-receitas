from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from models.models import SessionLocal,Receita,Usuario
from schemas import ReceitaOut,CriarReceita,Atualizar,LoginRequest,RegisterRequest
from typing import List
from fastapi.responses import RedirectResponse

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Retorna todas as receitas cadastradas
@router.get('/receber',response_model=List[ReceitaOut])
def receber(db: Session = Depends(get_db)):
    return db.query(Receita).all()

# Atualiza uma receita existente pelo ID
@router.put('/trocar/{id}',response_model=ReceitaOut)
def trocar(id: int,at: Atualizar,db: Session = Depends(get_db)):
    receita = db.query(Receita).filter(Receita.id == id).first()
    if not receita:
        raise HTTPException(status_code=404,detail='receita nao encontrada')
    
    if at.nome_da_receita is not None:
        receita.nome_da_receita = at.nome_da_receita
    if at.ingredientes is not None:
        receita.ingredientes = at.ingredientes
    if at.modo_de_preparo is not None:
        receita.modo_de_preparo = at.modo_de_preparo

    db.commit()
    db.refresh(receita)
    return receita

# Deleta uma receita pelo ID
@router.delete('/delete/{id}')
def deletar(id: int,db: Session = Depends(get_db)):
    receita = db.query(Receita).filter(Receita.id == id).first()
    if not receita:
        raise HTTPException(status_code=404,detail='receita nao encontrada')
    
    db.delete(receita)
    db.commit()
    return {'mensagem':'receita apagada com sucesso'}

# Retorna uma receita específica pelo ID
@router.get('/especifico/{id}',response_model=ReceitaOut)
def espefico(id: int,db: Session = Depends(get_db)):
    receita = db.query(Receita).filter(Receita.id == id).first()
    if not receita:
        raise HTTPException(status_code=404,detail='receita nao encontrada')
    return receita
