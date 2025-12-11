from fastapi import APIRouter, Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.models_usuario import Usuario
import requests  # ✅ substitui o language_tool_python

# ======================== Configurações de Autenticação ========================
# Chave secreta usada para assinar os tokens JWT. Em produção, deve ser obtida via
# variável de ambiente e nunca hardcoded no código.
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"  # Algoritmo de assinatura do JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração do token em minutos

# Contexto de hashing de senhas usando bcrypt. O 'deprecated="auto"' garante
# compatibilidade com versões antigas de hash.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Middleware de segurança para extrair credenciais do header Authorization.
security = HTTPBearer()

# ------------------- Funções de Autenticação -------------------

def verify_password(plain, hashed):
    """Verifica se a senha em texto plano corresponde ao hash armazenado."""
    return pwd_context.verify(plain, hashed)


def create_token(data: dict, expires_delta: timedelta = None):
    """
    Cria um JWT contendo os dados do usuário.
    - 'data' deve incluir pelo menos o campo 'sub' (subject/username).
    - O token expira após 'expires_delta' ou pelo tempo padrão configurado.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    """
    Decodifica um JWT e retorna o campo 'sub' (username).
    Retorna None se o token for inválido ou não decodificável.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def authenticate_user(db: Session, username: str, password: str):
    """
    Autentica um usuário consultando o banco:
    - Busca pelo username.
    - Verifica se a senha fornecida corresponde ao hash armazenado.
    Retorna o objeto Usuario se válido, ou None caso contrário.
    """
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Middleware de validação de token JWT:
    - Decodifica o token recebido no header Authorization.
    - Retorna o username se válido.
    - Lança HTTPException 401 em caso de token inválido ou expirado.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return username
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado, realize login novamente"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

# ======================== Funções de Correção de Texto ========================

def capitalizar_frases(texto: str) -> str:
    """
    Coloca letra maiúscula no início de cada frase.
    - Divide o texto por pontos.
    - Remove espaços extras.
    - Capitaliza cada frase.
    """
    frases = [f.strip().capitalize() for f in texto.split('.')]
    return '. '.join(frases).strip()


def corrigir_texto(texto: str) -> str:
    """
    Corrige ortografia usando a API pública do LanguageTool.
    - Envia o texto para a API (pt-BR).
    - Aplica correções sugeridas de trás para frente (para não quebrar offsets).
    - Capitaliza frases após correção.
    - Em caso de erro na API, apenas capitaliza.
    """
    url = "https://api.languagetool.org/v2/check"
    data = {
        "text": texto,
        "language": "pt-BR"
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()

        # Aplica correções de trás para frente para preservar índices
        for match in reversed(result.get('matches', [])):
            offset = match['offset']
            length = match['length']
            replacements = match.get('replacements', [])
            replacement = replacements[0]['value'] if replacements else ''
            texto = texto[:offset] + replacement + texto[offset + length:]

        return capitalizar_frases(texto)

    except Exception as e:
        print(f"Erro ao corrigir texto: {e}")
        return capitalizar_frases(texto)
