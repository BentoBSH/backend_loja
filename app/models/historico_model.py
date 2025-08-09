# backend_flask/app/models/historico_model.py

# Importa o ORM SQLAlchemy já configurado
from app import db

# Define a classe historico como modelo ORM
class Historico(db.Model):
    # Nome da tabela na base de dados
    __tablename__ = 'historico'

    id = db.Column(db.Integer, primary_key=True)
    id_utilizador = db.Column(db.Integer, db.ForeignKey('utilizador.id'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    data_compra = db.Column(db.Integer, nullable=False)

    # Relacionamentos
    utilizador = db.relationship('Utilizador', back_populates='historico')
    produto = db.relationship('Produto', back_populates='historico')


    # Representação para debug e logs
    def __repr__(self):
        return f"<historico {self.id_utilizador} - {self.id_produto} - {self.data_compra}>" 