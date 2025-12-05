import os
from dotenv import load_dotenv

load_dotenv()            # Carrega as variáveis definidas no arquivo .env para o ambiente do sistema

class Settings:          # Define uma classe chamada 'Settings' para centralizar configurações do projeto

    DATABASE_URL: str = os.getenv('DATABASE_URL')  
    # Cria um atributo chamado 'DATABASE_URL' e atribui o valor da variável de ambiente 'DATABASE_URL'.
    # O ': str' é uma anotação de tipo, indicando que o valor esperado é uma string.

settings = Settings()    # Instancia a classe 'Settings', criando um objeto com as configurações carregadas
