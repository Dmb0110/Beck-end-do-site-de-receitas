
'''
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


'''



from fastapi import FastAPI
from app.database.session import Base, engine
#from app.crud import router as crud_router
from fastapi.middleware.cors import CORSMiddleware
#from autenticacao10.jwt_auth2 import router as jwt_router
from app.router import api_router

app = FastAPI()

# Middleware para permitir requisições do frontend hospedado na Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://receitasmasterchef.vercel.app"],  # Substitua pela URL real do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Rotas principais da API
app.include_router(api_router)
#app.include_router(jwt_router)


'''


    
    def receber_cliente_conta(self, cliente_id: int) -> ReceitaOut:
        """
        Busca um cliente pelo ID e retorna junto com suas contas.
        Lança 404 se não encontrado.
        """
        receita = self.db.query(Receita).filter(Receita.id == receita_id).first()
        if not receita:
            raise HTTPException(status_code=404, detail="Receita não encontrada")
        return ClienteComContasSchema.model_validate(receita)
    


    
    def enviar(self, criar: CriarReceita) -> ReceitaOut:
        """
        Cria um novo cliente no banco.
        - `criar`: dados validados pelo schema CriarCliente.
        Retorna o cliente criado como ClienteOut.
        """
        nova_receita = Receita(**criar.model_dump())
        self.db.add(nova_receita)
        self.db.commit()
        self.db.refresh(nova_receita)  # garante que atributos gerados (ex: id) sejam carregados
        return ReceitaOut.model_validate(nova_receita)
    


@router.get(
    "/{cliente_id}",
    summary="Mostra dados do cliente e suas contas",
    response_model=ClienteComContasSchema,
    status_code=status.HTTP_200_OK
)
def receber_cliente_conta(cliente_id: int, service: ClienteService = Depends()):
    """
    Busca um cliente específico pelo ID e retorna junto com suas contas.
    Lança 404 se não encontrado.
    """
    return service.receber_cliente_conta(cliente_id)





@router.post(
    "/",
    summary="Criar receita",
    response_model=ReceitaOut,
    status_code=status.HTTP_201_CREATED
)
def criar_receita(criar: CriarReceita, service: ReceitaService = Depends()):
    """
    Cria um novo cliente.
    - `criar`: dados validados pelo schema CriarCliente.
    - `service`: instância de ClienteService injetada via Depends.
    Retorna o cliente criado como ClienteOut.
    """
    return service.enviar(criar)









LIXO DO FRONT CADASTRAR.HTML DO SITE DE RECEITA
{


const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app";


fetch(`${API_BASE}/enviar`, { ... })









  <script>
    const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app";

    async function criarReceita(dados) {
      const token = localStorage.getItem("access_token");

      if (!token) {
        alert("Você precisa estar logado para cadastrar uma receita.");
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/enviar`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(dados)
        });

        const result = await res.json();

        if (!res.ok) {
          alert(result.detail || "Erro ao salvar receita.");
          return;
        }

        alert("Receita cadastrada com sucesso!");
        window.location.href = "index4.html";
      } catch (error) {
        alert("Erro de conexão com o servidor.");
      }
    }

    async function handleCriar() {
      const nome = document.getElementById("nome").value;
      const ingredientes = document.getElementById("ingredientes").value;
      const modo = document.getElementById("modo").value;
      const btn = document.getElementById("btnSalvar");
      const loading = document.getElementById("loading");

      if (!nome || !ingredientes || !modo) {
        alert("Preencha todos os campos!");
        return;
      }

      btn.disabled = true;
      loading.style.display = "block";

      const novaReceita = {
        nome_da_receita: nome,
        ingredientes,
        modo_de_preparo: modo
      };

      await criarReceita(novaReceita);

      btn.disabled = false;
      loading.style.display = "none";
    }
  </script>









  <script>
    const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app/enviar";

    async function criarReceita(dados) {
      const token = localStorage.getItem("access_token");

      if (!token) {
        alert("Você precisa estar logado para cadastrar uma receita.");
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/enviar`, {






  <script>
    const API_BASE = "http://localhost:8000";

    function getIdFromURL() {
      const params = new URLSearchParams(window.location.search);
      return params.get("id");
    }

    async function buscarReceitaPorId(id) {
      const res = await fetch(`${API_BASE}/especifico/${id}`);
      if (!res.ok) throw new Error("Erro ao buscar receita");
      return await res.json();
    }

    async function carregarDetalhes() {
      const id = getIdFromURL();
      const receita = await buscarReceitaPorId(id);

      document.getElementById("titulo-receita").textContent = receita.nome_da_receita;

      const ingredientes = receita.ingredientes.split(",").map(i => i.trim()).filter(i => i !== "");
      const lista = document.getElementById("lista-ingredientes");
      ingredientes.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        lista.appendChild(li);
      });

      document.getElementById("modo-preparo").textContent = receita.modo_de_preparo;
    }

    carregarDetalhes();
  </script>



}











FROM python:3.11-slim

# Instala Java para language_tool_python
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk-headless \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia apenas os arquivos do backend
COPY main.py .
COPY models/ models/
COPY schemas.py .
COPY crud.py .
COPY autenticacao10/ autenticacao10/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]






services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: 'postgresql://neondb_owner:npg_HDj9psUF4Scv@ep-red-meadow-acf8hr0w-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'




 Exemplo de chamada
fetch("https://meu-back.vercel.app/api/login", {
  method: "POST",
  body: JSON.stringify({ email, senha }),
  headers: { "Content-Type": "application/json" }
})




services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: davi9090
      POSTGRES_DB: banco_dmb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:  # renomeado de "web" para "backend" para refletir melhor o propósito
    build: .
    depends_on:
      - db
    ports:
      - "8000:8000"  # ajuste conforme a porta usada pela sua API
    environment:
      DATABASE_URL: postgresql://postgres:davi9090@db:5432/banco_dmb

volumes:
  pgdata:





services:
  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: davi9090
      POSTGRES_DB: banco_dmb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  web:
    build: .
    depends_on:
      - db
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:davi9090@db:5432/banco_dmb

volumes:
  pgdata:




  



  FROM python:3.11-slim

# Instala dependências do sistema, incluindo Java
RUN apt-get update && apt-get install -y \
    openjdk-21-jdk-headless \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY front3/ front3/
COPY main.py .
COPY models.py models.py
COPY schemas.py schemas.py
COPY crud.py crud.py
COPY autenticacao10/ autenticacao10/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



'''



