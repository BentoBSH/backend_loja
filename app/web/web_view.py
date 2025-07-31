# backend_flask/app/web/web_view.py

from flask import Blueprint, render_template, request, jsonify
from app.controllers.utilizador_controller import UtilizadorController
from app.controllers.produto_controller import ProdutoController
from config import Config  # Garante que config.py está a ser usado

# Define o blueprint para rotas da Web
web = Blueprint("web", __name__)

def verificar_api_key():
    chave = request.headers.get("x-api-key")
    return chave == Config.API_KEY


# Página principal que mostra a lista de utilizadores
@web.route("/utilizadores")
def pagina_principal_utilizadores():
    if not verificar_api_key():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401
    # Obtém todos os utilizadores através do controller
    utilizadores = UtilizadorController.listar()

    # Renderiza o template HTML com os dados dos utilizadores
    return render_template("lista_utilizadores.html", utilizadores=utilizadores)

@web.route("/")
def pagina_principal():
    # Obtém todos os produtos através do controller
    produtos = ProdutoController.listar()

    # Renderiza o template HTML com os dados dos produtos
    return render_template("lista_produtos.html", produtos=produtos)