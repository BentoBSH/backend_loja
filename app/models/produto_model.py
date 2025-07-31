# backend_flask/app/models/produto_model.py

# Importa o ORM SQLAlchemy já configurado
from app import db

# Define a classe Produto como modelo ORM
class Produto(db.Model):
    # Nome da tabela na base de dados
    __tablename__ = 'produto'

    # Colunas da tabela
    id = db.Column(db.Integer, primary_key=True)             # Chave primária
    nome = db.Column(db.String(100), nullable=False)         # Nome obrigatório
    preco = db.Column(db.Integer, nullable=False)        # preco obrigatório
    estoque = db.Column(db.Integer, nullable=False)        # estoques obrigatório
    capa = db.Column(db.String, nullable=False)         #link da capa 
    fotos = db.Column(db.String, nullable=True)         #link da capa 
    descricao = db.Column(db.String, nullable=True)        # descrição
    categoria = db.Column(db.String, nullable=False)        # categoria
    detalhes = db.Column(db.String, nullable=True)        # detalhes
    comentarios = db.Column(db.String, nullable=True)        # comentários
    rate = db.Column(db.Integer, nullable=True)        # rate 

    # Construtor da classe (opcional, útil para criação manual de objetos)
    def __init__(self, nome, preco, capa, estoque, fotos, descricao, detalhes, categoria, comentarios, rate ):
        self.nome = nome
        self.preco = preco
        self.capa = capa
        self.estoque = estoque
        self.fotos = fotos
        self.descricao = descricao
        self.detalhes = detalhes
        self.categoria = categoria
        self.comentarios = comentarios
        self.rate = rate


    # Representação para debug e logs
    def __repr__(self):
        return f"<Produto {self.id} - {self.nome}> - {self.preco}> - {self.capa}> - {self.estoque}> - {self.categoria}>"
