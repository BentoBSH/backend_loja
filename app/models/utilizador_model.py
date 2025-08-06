# backend_flask/app/models/utilizador_model.py

# Importa o ORM SQLAlchemy já configurado
from app import db
from sqlalchemy.orm import relationship

# Define a classe Utilizador como modelo ORM
class Utilizador(db.Model):
    # Nome da tabela na base de dados
    __tablename__ = 'utilizador'

    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)             # Chave primária
    nome = db.Column(db.String(100), nullable=False)         # Nome obrigatório
    email = db.Column(db.String(100), nullable=False)        # Email obrigatório
    palavra_passe = db.Column(db.String(200), nullable=False)        # Password obrigatório
    carrinho = db.relationship('Carrinho', back_populates='utilizador', cascade="all, delete", lazy=True)
    grupo = db.Column(db.Integer, nullable=False)        # Grupo obrigatório

    # Construtor da classe (opcional, útil para criação manual de objetos)
    def __init__(self, nome, email, grupo, palavra_passe, carrinho):
        self.nome = nome
        self.email = email
        self.grupo = grupo
        self.palavra_passe = palavra_passe
        self.carrinho = carrinho


    # Representação para debug e logs
    def __repr__(self):
        return f"<Utilizador {self.id} - {self.nome} - {self.grupo} - {self.carrinho}>" 