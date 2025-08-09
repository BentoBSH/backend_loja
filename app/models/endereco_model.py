# backend_flask/app/models/endereco_model.py

# Importa o ORM SQLAlchemy já configurado
from app import db

# Define a classe endereco como modelo ORM
class Endereco(db.Model):
    # Nome da tabela na base de dados
    __tablename__ = 'endereco'

    id = db.Column(db.Integer, primary_key=True)
    id_utilizador = db.Column(db.Integer, db.ForeignKey('utilizador.id'), nullable=False)
    email = db.Column(db.String, nullable=False)
    telefone = db.Column(db.Integer, nullable=False)
    municipio = db.Column(db.String, nullable=False)
    detalhes_rua = db.Column(db.String, nullable=False)

    # Relacionamentos
    utilizador = db.relationship('Utilizador', back_populates='endereco')


    # Representação para debug e logs
    def __repr__(self):
        return f"<endereco: {self.municipio} - {self.email} - {self.telefone} - {self.detalhes_rua}>" 