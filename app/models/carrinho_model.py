# backend_flask/app/models/carrinho_model.py

# Importa o ORM SQLAlchemy já configurado
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Define a classe Carrinho como modelo ORM
class Carrinho(db.Model):
    # Nome da tabela na base de dados
    __tablename__ = 'carrinho'

    id = db.Column(db.Integer, primary_key=True)
    id_utilizador = db.Column(db.Integer, db.ForeignKey('utilizador.id'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    # Relacionamentos
    utilizador = db.relationship('Utilizador', back_populates='carrinho')
    produto = db.relationship('Produto', back_populates='carrinho')

    '''
        # Construtor da classe (opcional, útil para criação manual de objetos)
        def __init__(self, id_utilizador, id_produtos, quantidade):
            self.utilizador = utilizador
            self.id_utilizador = id_utilizador
            self.produtos = produtos
            self.quantidade = quantidade
    '''

    # Representação para debug e logs
    def __repr__(self):
        return f"<Carrinho {self.id_utilizador} - {self.id_produto} - {self.quantidade}>" 