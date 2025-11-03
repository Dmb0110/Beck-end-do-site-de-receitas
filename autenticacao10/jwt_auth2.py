from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from models.models import Usuario,Receita
from crud import get_db
from schemas import LoginRequest,ReceitaOut,CriarReceita,RegisterRequest
import language_tool_python

router = APIRouter()

# Configurações do JWT
SECRET_KEY = "sua_chave_secreta"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verifica se a senha fornecida corresponde ao hash armazenado
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Gera um token JWT com tempo de expiração
def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decodifica o token JWT e retorna o campo 'sub'
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

# Autentitica o usuário comparando credenciais com o banco
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

# verifica se o token JWT está presente e válido
def verificar_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou mal formatado")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado,realize login novamente")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Endpoint de login: retorna token se credenciais forem válidas
@router.post("/login10")
async def login(request: LoginRequest,db: Session = Depends(get_db)):
    username = request.username
    password = request.password

    user = authenticate_user(db,username,password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_token({"sub": username})
    return {"access_token": token}

#Endpoint de registro de novo usuário
@router.post("/register", status_code=201)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=401, detail="Usuário já existe")

    hashed_password = pwd_context.hash(request.password)
    novo_usuario = Usuario(
        username=request.username,
        password=hashed_password,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {"msg": "Usuário registrado com sucesso"}


# Inicializa o corretor para português do Brasil
tool = language_tool_python.LanguageTool('pt-BR')

def corrigir_texto(texto: str) -> str:
    """Corrige ortografia e aplica capitalização no início de frases."""
    texto_corrigido = tool.correct(texto)
    return capitalizar_frases(texto_corrigido)

def capitalizar_frases(texto: str) -> str:
    """Coloca letra maiúscula no início de cada frase."""
    frases = texto.split('. ')
    frases_formatadas = [frase.capitalize() for frase in frases]
    return '. '.join(frases_formatadas)

@router.post('/enviar', response_model=ReceitaOut)
def enviar(request: Request, criar: CriarReceita, db: Session = Depends(get_db)):
    username = verificar_token(request)

    # Aplica correção ortográfica e capitalização nos campos textuais
    criar.nome_da_receita = corrigir_texto(criar.nome_da_receita)
    criar.ingredientes = corrigir_texto(criar.ingredientes)
    criar.modo_de_preparo = corrigir_texto(criar.modo_de_preparo)

    nova_receita = Receita(**criar.dict())
    db.add(nova_receita)
    db.commit()
    db.refresh(nova_receita)
    return nova_receita
