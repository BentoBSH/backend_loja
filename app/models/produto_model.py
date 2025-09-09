# backend_flask/app/models/produto_model.py

# Importa o ORM SQLAlchemy já configurado
from app import db

# Define a classe Produto como modelo ORM
class Produto(db.Model):
    # Nome da tabela na base de dados
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    capa = db.Column(db.String(300), nullable=False)
    fotos = db.Column(db.String(800))
    estoque = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(800), nullable=False)
    rate = db.Column(db.Integer)
    descricao = db.Column(db.String(1000))
    detalhes = db.Column(db.String(2000))
    comentarios = db.Column(db.String(4000))

    # Relacionamento com o carrinho
    #carrinho = db.relationship('Carrinho', back_populates='produto', cascade="all, delete", lazy=True)


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
