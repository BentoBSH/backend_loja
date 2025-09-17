# backend_flask/app/models/historico_model.py

# Importa o ORM SQLAlchemy já configurado
from app import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime, text

# Define a classe historico como modelo ORM
class Historico(db.Model):
    # Nome da tabela na base de dados
    __tablename__ = 'historico'

    id = db.Column(db.Integer, primary_key=True)
    id_utilizador = db.Column(db.Integer, db.ForeignKey('utilizador.id'), nullable=False)
    id_produtos = db.Column(db.String(255), nullable=False)
    quantidades = db.Column(db.String(255), nullable=False)
    data_compra = db.Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    id_compra = db.Column(db.String(255), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    detalhes = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.String(255), nullable=True)




    # Relacionamentos
    utilizador = db.relationship('Utilizador', back_populates='historico')


    # Representação para debug e logs
    def __repr__(self):
        return f"<historico {self.id_utilizador} - {self.id_produtos} - {self.id_compra}>" 
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_utilizador": self.id_utilizador,
            "id_produtos": self.id_produtos,
            "quantidades": self.quantidades,
            "data_compra": self.data_compra.isoformat() if self.data_compra else None, # Formata para string ISO 8601
            "id_compra": self.id_compra,
            "total": self.total,
            "detalhes": self.detalhes,
            "estado": self.estado
        }