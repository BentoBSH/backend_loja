from app import db
from sqlalchemy import DateTime, text

class Mensagem(db.Model):
    __tablename__ = "mensagem"

    id = db.Column(db.Integer, primary_key=True)
    id_utilizador = db.Column(db.Integer, db.ForeignKey("utilizador.id"), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    remetente = db.Column(db.String(50), nullable=False)  # "cliente" ou "admin"
    data_envio = db.Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    utilizador = db.relationship("Utilizador", back_populates="mensagens")

    def to_dict(self):
        return {
            "id": self.id,
            "id_utilizador": self.id_utilizador,
            "conteudo": self.conteudo,
            "remetente": self.remetente,
            "data_envio": self.data_envio.isoformat() if self.data_envio else None,
        }
