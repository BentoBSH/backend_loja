# backend_flask/app/routes/chat_routes.py
from flask import Blueprint, jsonify
from app.models.mensagem_model import Mensagem

chat_bp = Blueprint("chat", __name__)

# Histórico de um único cliente
@chat_bp.route("/chat/<int:id_utilizador>", methods=["GET"])
def get_historico_cliente(id_utilizador):
    mensagens = (
        Mensagem.query.filter_by(id_utilizador=id_utilizador)
        .order_by(Mensagem.data_envio)
        .all()
    )
    return jsonify([m.to_dict() for m in mensagens])


# Histórico completo (admin)
@chat_bp.route("/chat", methods=["GET"])
def get_historico_todos():
    mensagens = Mensagem.query.order_by(Mensagem.data_envio).all()
    return jsonify([m.to_dict() for m in mensagens])
