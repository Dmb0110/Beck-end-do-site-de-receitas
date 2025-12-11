import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

'''
pytest -s -v tests/test_post_auth_receita.py

'''

@pytest.fixture
def token_valido():
    # Registra um usuário
    usuario = {"username": "admin15", "password": "1234"}
    client.post("/registro/registro", json=usuario)

    # Faz login e pega o token
    response = client.post("/login/login", json=usuario)
    data = response.json()
    return data["access_token"]

def test_criar_auth(token_valido):
    nova_receita = {
    "nome_da_receita": "Receita",
    "ingredientes": "Receita",
    "modo_de_preparo":"Receita"
    }
    response = client.post(
        "/receita_auth/enviar",  # rota de criação de cliente
        json=nova_receita,
        headers={"Authorization": f"Bearer {token_valido}"}
    )
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["nome_da_receita"] == "Receita"
    assert data['ingredientes'] == "Receita"
    assert data['modo_de_preparo'] == "Receita"

    print('TESTE BEM SUCEDIDO,RECEITA CRIADA COM AUTENTICACAO COM SUCESSO')

