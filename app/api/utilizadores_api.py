# backend_flask/app/api/api_view.py

from flask import Blueprint, request, jsonify, make_response
from app.controllers.utilizador_controller import UtilizadorController
from config import Config  # Garante que config.py está a ser usado
import jwt
from datetime import datetime, timedelta, timezone
from argon2 import PasswordHasher
from app.api.email_api import enviar_email_novo_usuario
from flask_cors import cross_origin 

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

# Rota para logar o utilizador
@utilizadores.route("/utilizadores/login", methods=["POST"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def login_utilizadores():
    cookie_sessao = request.cookies.get('cookie_sessao')
    email = request.json.get('email', None)
    palavra_passe = request.json.get('palavra_passe', None)

    if cookie_sessao: 
        try:
        # Extrair o token do cabeçalho "Bearer <token>"
            token = cookie_sessao
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            decoded_token["exp"] = datetime.now(timezone.utc) + timedelta(hours=168) # atualiza a expiração do Token em horas
            encoded_token = jwt.encode(decoded_token, Config.SECRET_KEY, 'HS256')
            

            # Cria uma resposta Flask (necessário para adicionar cookies)
            response = make_response(jsonify({'message': 'Bem vindo de volta', 'user_info': encoded_token}))
            
            response.set_cookie(
                'cookie_sessao',
                encoded_token,
                max_age=604800,  # 7 dias (em segundo)
                path='/',
                secure=True, # Alterar para True em produção (HTTPS)
            )

            return response, 200
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invalido'}), 401
        except IndexError:
            return jsonify({'message': 'Formato de token inválido.', 'cookie': cookie_sessao}), 401

    if not email or not palavra_passe:
        return jsonify({"erro": "email e password são obrigatórios"}), 401
    
    # Verificação de credenciais
    
    uDB = UtilizadorController.obter_via_email(email)
    u = uDB
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
            'exp': datetime.now(timezone.utc) + timedelta(hours=168) # Token expira em horas
        }
        token = jwt.encode(token_payload, Config.SECRET_KEY, algorithm='HS256')

        # envia um email ao usuário 

        # Cria uma resposta Flask (necessário para adicionar cookies)
        response = make_response(jsonify({'message': 'Acesso concedido', 'user_info': token}))
        
        response.set_cookie(
            'cookie_sessao',
            token,
            max_age=604800,  # 1 hora
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
        u= uDB
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



# Rota para obter o endereço do utilizador
@utilizadores.route("/utilizadores/endereco", methods=["GET"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def obter_endereco():

    cookie_sessao = request.cookies.get('cookie_sessao')
    if not cookie_sessao:
        return jsonify({"erro": "Acesso não autorizado – Não tem sessão ativa"}), 401

    decoded_token = jwt.decode(cookie_sessao, Config.SECRET_KEY, algorithms=['HS256'])
    id = decoded_token["user_id"]

    endereco = UtilizadorController.obter_endereco(id)
    if endereco:
        return jsonify([
        {"nome": endereco.nome, "email": endereco.email, "telefone": endereco.telefone, "municipio": endereco.municipio,"detalhes_rua": endereco.detalhes_rua} 
    ])
    return jsonify([
        {"erro": "não foi encontrado qualquer registro de endereço"} 
    ]), 404

# Rota para atualizar endereço
@utilizadores.route("/utilizadores/endereco", methods=["PUT"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def atualizar_endereco():

    cookie_sessao = request.cookies.get('cookie_sessao')
    if not cookie_sessao:
        return jsonify({"erro": "Acesso não autorizado – Não tem sessão ativa"}), 401

    decoded_token = jwt.decode(cookie_sessao, Config.SECRET_KEY, algorithms=['HS256'])
    id = decoded_token["user_id"]

    dados = request.get_json()
    email = dados.get("email")
    telefone = dados.get("telefone")
    municipio = dados.get("municipio")
    detalhes_rua = dados.get("detalhes_rua")

    endereco = UtilizadorController.atualizar_endereco(id, email, telefone, municipio, detalhes_rua)

    return jsonify([
        {"nome": endereco.nome, "email": endereco.email, "telefone": endereco.telefone, "municipio": endereco.municipio,"detalhes_rua": endereco.detalhes_rua} 
    ])


# Rota para listar carrinho do utilizador
@utilizadores.route("/utilizadores/carrinho", methods=["GET"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def listar_carrinho():

    cookie_sessao = request.cookies.get('cookie_sessao')
    if not cookie_sessao:
        return jsonify({"erro": "Acesso não autorizado – Não tem sessão ativa"}), 401

    decoded_token = jwt.decode(cookie_sessao, Config.SECRET_KEY, algorithms=['HS256'])
    id = decoded_token["user_id"]

    utilizadores = UtilizadorController.obter(id)
    print(decoded_token)
    return jsonify([
        {"produto": u.produto.nome, "id produto": u.id_produto, "quantidade": u.quantidade} for u in utilizadores.carrinho
    ])

# Adicionar item ao carrinho
@utilizadores.route("/utilizadores/carrinho", methods=["post"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def adicionar_ao_carrinho():

    cookie_sessao = request.cookies.get('cookie_sessao')
    if not cookie_sessao:
        return jsonify({"erro": "Acesso não autorizado – Não tem sessão ativa"}), 401

    decoded_token = jwt.decode(cookie_sessao, Config.SECRET_KEY, algorithms=['HS256'])
    id = decoded_token["user_id"]

    dados = request.get_json()
    produto = dados.get("id_produto")
    quantidade = dados.get("quantidade")

    carrinho = UtilizadorController.adicionar_no_carrinho(id, produto, quantidade)

    return jsonify([
        {"id do produto adicionado": carrinho.id_produto, "quantidade": carrinho.quantidade} 
    ])



# Atualizar carrinho
@utilizadores.route("/utilizadores/carrinho", methods=["put"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def atualizar_o_carrinho():

    cookie_sessao = request.cookies.get('cookie_sessao')
    if not cookie_sessao:
        return jsonify({"erro": "Acesso não autorizado – Não tem sessão ativa"}), 401

    decoded_token = jwt.decode(cookie_sessao, Config.SECRET_KEY, algorithms=['HS256'])
    id = decoded_token["user_id"]

    dados = request.get_json()
    produto = dados.get("id_produto")
    quantidade = dados.get("quantidade")

    carrinho = UtilizadorController.atualizar_carrinho(id, produto, quantidade)
    return jsonify([
        {"id do produto adicionado": carrinho.id_produto, "quantidade": carrinho.quantidade} 
    ])

# Deletar item do carrinho
@utilizadores.route("/utilizadores/carrinho", methods=["delete"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def deletar_do_carrinho():

    cookie_sessao = request.cookies.get('cookie_sessao')
    if not cookie_sessao:
        return jsonify({"erro": "Acesso não autorizado – Não tem sessão ativa"}), 401

    decoded_token = jwt.decode(cookie_sessao, Config.SECRET_KEY, algorithms=['HS256'])
    id = decoded_token["user_id"]

    dados = request.get_json()
    produto = dados.get("id_produto")

    carrinho = UtilizadorController.remover_do_carrinho(id, produto)

    return jsonify([
        {"id do produto deletado": produto, "deletado": carrinho} 
    ])


# Adicionar historico de compra
@utilizadores.route("/utilizadores/historico", methods=["post"])
@cross_origin(supports_credentials=True) # aceitar credeciais, cuidado credenciais podem ser imbutidas na requisição 
def adicionar_ao_historico():
    print(request.cookies)
    cookie_sessao = request.cookies.get('cookie_sessao')
    if not cookie_sessao:
        return jsonify({"erro": "Acesso não autorizado – Não tem sessão ativa"}), 401

    decoded_token = jwt.decode(cookie_sessao, Config.SECRET_KEY, algorithms=['HS256'])
    id = decoded_token["user_id"]

    dados = request.get_json()
    #id = dados.get("id")
    id_produtos = dados.get("id_produtos")
    quantidades = dados.get("quantidades")
    id_compra = dados.get("id_compra")


    historico = UtilizadorController.adicionar_ao_historico(id, id_produtos, quantidades, id_compra)

    return jsonify([
        {"id dos produtos adicionados ao historico": historico.id_produtos} 
    ])