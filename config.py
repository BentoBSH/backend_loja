import os
from dotenv import load_dotenv

# Carrega o .env relativo ao local deste ficheiro
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

class Config:

    API_KEY = os.getenv("API_KEY")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqldb://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        f"?ssl_ca={os.getenv('SSL_CERTIFICADO')}"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": os.getenv("SSL_CERTIFICADO")
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'chave-default'
    EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    SMTP_SERVIDOR = os.getenv('SMTP_SERVIDOR')
    SMTP_PORTA = os.getenv('SMTP_PORTA')