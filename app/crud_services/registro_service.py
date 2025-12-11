from fastapi import HTTPException
from app.models.models_usuario import Usuario
from app.schemas.schemas import RegisterRequest
from sqlalchemy.orm import Session
from app.autenticacao10.jwt_auth2 import pwd_context

class RegistroService:
    """
    Serviço responsável pelo processo de registro de novos usuários.
    - Encapsula a lógica de persistência e validação.
    - Utiliza SQLAlchemy para interação com o banco.
    - Usa Pydantic (RegisterRequest) para validação de entrada.
    """

    @staticmethod
    def registrar_usuario(request: RegisterRequest, db: Session) -> dict:
        """
        Registra um novo usuário no sistema.
        
        Fluxo:
        1. Verifica se já existe um usuário com o mesmo username.
           - Se existir, lança HTTPException 400.
        2. Gera o hash da senha usando bcrypt (via pwd_context).
        3. Cria uma instância de Usuario e persiste no banco.
        4. Retorna mensagem de sucesso.

        Args:
            request (RegisterRequest): Dados de entrada (username, password).
            db (Session): Sessão do banco de dados.

        Returns:
            dict: Mensagem confirmando o registro.
        """

        # Verifica se o username já está em uso
        existing_user = db.query(Usuario).filter(Usuario.username == request.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Usuário já existe")

        # Gera hash seguro da senha
        hashed_password = pwd_context.hash(request.password)

        # Cria novo usuário com username e senha criptografada
        novo_usuario = Usuario(username=request.username, password=hashed_password)

        # Persiste no banco
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        # Retorna mensagem de sucesso
        return {"mensagem": "Usuário registrado com sucesso"}
