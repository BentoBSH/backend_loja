# backend_flask/app/sockets.py
from flask_socketio import SocketIO, emit, join_room
from app import db
from app.models.mensagem_model import Mensagem

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("join")
def handle_join(data):
    """
    Cliente ou admin entra em uma sala (room).
    Exemplo de data:
    {"room": "1"} -> sala do cliente 1
    {"room": "admin"} -> sala do admin que vê todos
    """
    room = str(data["room"])
    join_room(room)
    emit("status", {"msg": f"Entrou na sala {room}"}, room=room)


@socketio.on("send_message")
def handle_message(data):
    """
    data esperado:
    {
        "id_utilizador": 1,
        "conteudo": "Olá!",
        "remetente": "cliente" ou "admin",
        "room": "1"
    }
    """
    try:
        nova_msg = Mensagem(
            id_utilizador=data["id_utilizador"],
            conteudo=data["conteudo"],
            remetente=data["remetente"],
        )
        db.session.add(nova_msg)
        db.session.commit()

        # envia para a sala do cliente e também para "admin"
        emit("receive_message", nova_msg.to_dict(), room=data["room"])
        emit("receive_message", nova_msg.to_dict(), room="admin")
    except Exception as e:
        db.session.rollback()
        print("Erro ao salvar mensagem:", e)
