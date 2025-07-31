# backend_flask/app/api/api_view.py

from flask import Blueprint, request, jsonify, make_response
from app.controllers.utilizador_controller import UtilizadorController
from config import Config  # Garante que config.py está a ser usado
import jwt
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from app.api.email_view import enviar_email_novo_usuario

ph = PasswordHasher()

# Define o blueprint para rotas da API
utilizadores = Blueprint("utilizadores", __name__)

# Função para verificar a API Key enviada no cabeçalho
def verificar_api_key():
    chave = request.headers.get("x-api-key")
    return chave == Config.API_KEY

def verificar_api_key_super():
    chave = request.headers.get("super-api-key")
    return chave == Config.API_KEY

# Rota para listar todos os utilizadores
@utilizadores.route("/utilizadores/login", methods=["POST"])
def login_utilizadores():
    cookie_sessao = request.cookies.get('cookie_sessao')
    email = request.json.get('email', None)
    palavra_passe = request.json.get('palavra_passe', None)

    if cookie_sessao: 
        try:
        # Extrair o token do cabeçalho "Bearer <token>"
            token = cookie_sessao
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])

            # Cria uma resposta Flask (necessário para adicionar cookies)
            response = make_response(jsonify({'message': 'Acesso concedido', 'user_info': decoded_token}))
            
            response.set_cookie(
                'cookie_sessao',
                token,
                max_age=3600,  # 1 hora
                path='/',
                secure=False, # Altere para True em produção (HTTPS)
            )

            return response, 200
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        except IndexError:
            return jsonify({'message': 'Formato de token inválido.', 'cookie': cookie_sessao}), 401

    if not email or not palavra_passe:
        return jsonify({"erro": "email e password são obrigatórios"}), 401
    
    # Verificação de credenciais
    
    uDB = UtilizadorController.obter_via_email(email)
    u = uDB[0]
    if not u:
        return jsonify({"erro": 'Credenciais inválidas'}), 401
 
    try:
        password_true = ph.verify(u.palavra_passe, palavra_passe)
        password = password_true
    except Exception as e:
        password = False

    if password:
        # Gerar o token JWT
        token_payload = {
            'user_id': u.id,
            'email': email,
            'exp': datetime.now(timezone.utc) + timedelta(hours=72) # Token expira em horas
        }
        token = jwt.encode(token_payload, Config.SECRET_KEY, algorithm='HS256')

        # envia um email ao usuário 

        # Cria uma resposta Flask (necessário para adicionar cookies)
        response = make_response(jsonify({'message': 'Login bem-sucedido'}))
        
        response.set_cookie(
            'cookie_sessao',
            token,
            max_age=3600,  # 1 hora
            path='/',
            secure=False, # Altere para True em produção (HTTPS)
        )

        return response, 200

    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401


# Rota para listar todos os utilizadores
@utilizadores.route("/utilizadores", methods=["GET"])
def listar_utilizadores():
    if not verificar_api_key():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401

    utilizadores = UtilizadorController.listar()
    return jsonify([
        {"id": u.id, "nome": u.nome, "email": u.email, "grupo": u.grupo} for u in utilizadores
    ])

# Rota para obter um único utilizador por ID
@utilizadores.route("/utilizadores/id/<int:id_utilizador>", methods=["GET"])
def obter_utilizador(id_utilizador):
    if not verificar_api_key():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401
    
    uDB = UtilizadorController.obter(id_utilizador)
    if uDB:
        u= uDB[0]
        return jsonify({"id": u.id, "nome": u.nome, "grupo": u.grupo})
    return jsonify({"erro": "Utilizador não encontrado"}), 404

# Rota para obter um único utilizador por email
@utilizadores.route("/utilizadores/email/<email_utilizador>", methods=["GET"])
def obter_utilizador_por_email(email_utilizador):
    if not verificar_api_key():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401
    
    uDB = UtilizadorController.obter_via_email(email_utilizador)
    if uDB:
        u= uDB[0]
        return jsonify({"id": u.id, "nome": u.nome, "email": u.email, "grupo": u.grupo})
    return jsonify({"erro": "Utilizador não encontrado"}), 404


# Rota para criar um novo utilizador
@utilizadores.route("/utilizadores", methods=["POST"])
def criar_utilizador():
#    if not verificar_api_key():
#        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401

    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    palavra_passe_raw = dados.get("palavra_passe")
    ''' try:
        hash = ph.hash(palavra_passe_raw)
        palavra_passe = hash
    except Exception as e:
        palavra_passe = False
    '''
    palavra_passe = ph.hash(palavra_passe_raw)
    grupo = 4
    if not nome or not email:
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400
    novo = UtilizadorController.criar(nome, email, grupo, palavra_passe)
    enviar_email_novo_usuario(email)
    return jsonify({"id": novo.id, "nome": novo.nome, "email": novo.email, "grupo": novo.grupo}), 201

# Rota para atualizar um utilizador existente
@utilizadores.route("/utilizadores/<int:id_utilizador>", methods=["PUT"])
def atualizar_utilizador(id_utilizador):
    if not verificar_api_key():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401
    if not verificar_api_key_super():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    grupo = dados.get("grupo")
    palavra_passe = dados.get("palavra_passe")
    atualizado = UtilizadorController.editar(id_utilizador, nome, email, grupo, palavra_passe)
    if atualizado:
        return jsonify({"id": atualizado.id, "nome": atualizado.nome, "email": atualizado.email, "grupo": atualizado.grupo})
    return jsonify({"erro": "Utilizador não encontrado"}), 404

# Rota para apagar um utilizador
@utilizadores.route("/utilizadores/<int:id_utilizador>", methods=["DELETE"])
def apagar_utilizador(id_utilizador):
    if not verificar_api_key():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401
    if not verificar_api_key_super():
        return jsonify({"erro": "Acesso não autorizado – API Key inválida"}), 401
    sucesso = UtilizadorController.remover(id_utilizador)
    if sucesso:
        return jsonify({"mensagem": "Utilizador apagado com sucesso"})
    return jsonify({"erro": "Utilizador não encontrado"}), 404 
