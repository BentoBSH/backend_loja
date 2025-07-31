# backend_flask/app/api/api_view.py

from flask import Blueprint, request, jsonify, make_response
from app.controllers.produto_controller import ProdutoController

# Define o blueprint para rotas da API
produtos = Blueprint("produtos", __name__)

# Rota para listar todos os produtos
@produtos.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = ProdutoController.listar()
    response = make_response(jsonify([
        {"product_id": str(p.id), "nome": p.nome, "preco": p.preco, "capa": p.capa, "fotos": p.fotos, "estoque": p.estoque, "categoria": p.categoria, "rate": p.rate, "descricao": p.descricao, "detalhes": p.detalhes, "comentarios": p.comentarios} for p in produtos
    ]), 200) 
    return response

# Rota para listar todos os produtos com offsest e limit
@produtos.route("/produtos/offset/<int:offset>/<int:limit>", methods=["GET"])
def listar_produtos_com_offset(offset, limit):
    produtos = ProdutoController.listar_com_offset_limit(myOffset=offset, myLimit=limit)
    return jsonify([
        {"id": p.id, "nome": p.nome, "preco": p.preco} for p in produtos
    ])

    
# Rota para buscar produtos por nome
@produtos.route("/produtos/nome/<nome>", methods=["GET"])
def listar_produtos_por_nome(nome):
    produtos = ProdutoController.buscar_por_nome(nome_por_pesquisar=nome)
    return jsonify([
        {"id": p.id, "nome": p.nome, "preco": p.preco} for p in produtos
    ])
    
# Rota para buscar produtos por categoria | Dispositivos, componentes, acessorios, Outros, Best, Smartfone, Android, Computador, Laptop
@produtos.route("/produtos/categoria/<categoria>", methods=["GET"])
def listar_produtos_por_categoria(categoria):
    produtos = ProdutoController.buscar_por_categoria(nome_por_pesquisar=categoria)
    return jsonify([
        {"id": p.id, "nome": p.nome, "preco": p.preco} for p in produtos
    ])
    

# Rota para buscar produtos por preço 
@produtos.route("/produtos/preco/<int:preco_min>/<int:preco_max>", methods=["GET"])
def listar_produtos_por_preco(preco_min, preco_max):
    produtos = ProdutoController.listar_pelo_preco(menor_preco=preco_min, maior_preco=preco_max)
    return jsonify([
        {"id": p.id, "nome": p.nome, "preco": p.preco} for p in produtos
    ])


# Rota para obter um único produto por ID
@produtos.route("/produtos/id/<int:id_produto>", methods=["GET"])
def obter_produto(id_produto):
    p = ProdutoController.obter(id_produto)
    if p:
        return jsonify({"id": p.id, "nome": p.nome, "preco": p.preco})
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para criar um novo Produto  
@produtos.route("/produtos", methods=["POST"])
def criar_produto():
    dados = request.get_json()
    nome = dados.get("nome")
    preco = dados.get("preco")
    capa = dados.get("capa")
    fotos = dados.get("fotos")
    estoque = dados.get("estoque")
    categoria = dados.get("categoria")
    rate = dados.get("preco")
    descricao = dados.get("descricao")
    detalhes = dados.get("detalhes")
    comentario = dados.get("comentario")

    if not nome or not preco or not estoque or not capa or not categoria:
        return jsonify({"erro": "Nome, preço, estoque, capa e categoria são obrigatórios"}), 400
    novo = ProdutoController.criar(nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentario)
    return jsonify({"id": novo.id, "nome": novo.nome, "preco": novo.preco, "capa": novo.capa, "fotos": novo.fotos, "estoque": novo.estoque, "categoria": novo.categoria, "rate": novo.rate, "descricao": novo.descricao, "detalhes": novo.detalhes, "comentarios": novo.comentarios}), 201

# Rota para atualizar um produto existente
@produtos.route("/produtos/<int:id_produto>", methods=["PUT"])
def atualizar_produto(id_produto):
    dados = request.get_json()
    nome = dados.get("nome")
    preco = dados.get("preco")
    capa = dados.get("capa")
    fotos = dados.get("fotos")
    estoque = dados.get("estoque")
    categoria = dados.get("categoria")
    rate = dados.get("preco")
    descricao = dados.get("descricao")
    detalhes = dados.get("detalhes")
    comentarios = dados.get("comentarios")
    atualizado = ProdutoController.editar(id_produto, nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentarios)
    if atualizado:
        return jsonify({"id": atualizado.id, "nome": atualizado.nome, "preco": atualizado.preco, "capa": atualizado.capa, "fotos": atualizado.fotos, "estoque": atualizado.estoque, "categoria": atualizado.categoria, "rate": atualizado.rate, "descricao": atualizado.descricao, "detalhes": atualizado.detalhes, "comentarios": atualizado.comentarios})
    return jsonify({"erro": "produto não encontrado"}), 404

# Rota para apagar um produto
@produtos.route("/produtos/<int:id_produto>", methods=["DELETE"])
def apagar_produto(id_produto):
    sucesso = ProdutoController.remover(id_produto)
    if sucesso:
        return jsonify({"mensagem": "Produto apagado com sucesso"})
    return jsonify({"erro": "Produto não encontrado"}), 404
