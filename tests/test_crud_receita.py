import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

'''
COMANDOS PRA TESTAR COM PYTEST
pytest tests/test_crud.py

pytest -s -v tests/test_crud_receita.py

pytest

'''

'''
# ESSA ROTA NAO VAI FUNCIONAR NESSE PROJETO,
# JA EXISTE UMA ROTA (POST) PROTEGIDA
s
# Teste POST (criar recurso)
def test_criar_receita():
    nova_receita = {"nome_da_receita": "string", "ingredientes": "string","modo_de_preparo":"string"}
    response = client.post('/receita_auth/enviar', json=nova_receita)
    assert response.status_code == 201
    data = response.json()
    assert data["nome_da_receita"] == "string"
    assert data['ingredientes'] == 'string'
    assert data['modo_de_preparo'] == 'string'
    assert "id" in data
    print('TESTE BEM SUCEDIDO,RECEITA CRIADA COM SUCESSO')


# Teste GET (listar recurso)
def test_listar_receitas():
    response = client.get("/receita/receber")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

'''
# Teste GET (listar todos e imprimir todos)
def test_get():
    response = client.get("/receita/receber")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data,list)
    assert len(data) > 0
    print('\n [TESTE BEM SUCEDIDO,DADOS RETORNADOS]:')
    print(json.dumps(data,indent=2,ensure_ascii=False))
'''

# Teste PUT (atualizar recurso)
def test_atualizar_receita():
    receita_atualizada = {
    "nome_da_receita": "Receita",
    "ingredientes": "String",
    "modo_de_preparo":"String"
    }
    response = client.put("/receita/trocar/39", json=receita_atualizada)
    assert response.status_code == 200
    data = response.json()
    assert data["nome_da_receita"] == "Receita"
    assert data['ingredientes'] == 'String'
    assert data['modo_de_preparo'] == 'String'
    print('TESTE BEM SUCEDIDO,RECEITA ATUALIZADA COM SUCESSO')


# Teste DELETE (remover recurso)
def test_deletar_receita():
    response = client.delete("/receita/deletar/39")
    assert response.status_code == 200
    data = response.json()
    #assert data["mensagem"] == "RECEITA DELETADA COM SUCESSO"
    print('TESTE BEM SUCEDIDO,RECEITA DELETADA COM SUCESSO')
'''

