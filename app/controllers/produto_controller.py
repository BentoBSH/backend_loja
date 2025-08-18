# backend_flask/app/controllers/produto_controller.py

# Importa a camada DAO
from app.dao.produto_dao import ProdutoDAO

# Define a classe de controlo da lógica de negócio
class ProdutoController:

    @staticmethod
    def listar():
        """
        Retorna todos os produtos.
        """
        return ProdutoDAO.listar_todos()


    @staticmethod
    def listar_com_offset_limit(myOffset, myLimit):
        """
        Retorna produtos com offset e limit.
        """
        return ProdutoDAO.listar_todos_com_offset_limit(offset=myOffset, limit=myLimit)

    @staticmethod
    def buscar_por_nome(nome_por_pesquisar):
        """
        Retorna todos os produtos com nome semelhante.
        """
        return ProdutoDAO.listar_por_nome(nome_busca=nome_por_pesquisar)
    
    @staticmethod
    def buscar_por_categoria(categoria_por_pesquisar):
        """
        Retorna todos os produtos com nome semelhante.
        """
        return ProdutoDAO.listar_por_categoria(categoria_busca=categoria_por_pesquisar)


    @staticmethod
    def listar_pelo_preco(menor_preco, maior_preco):
        """
        Retorna produtos por uma range de preço.
        """
        return ProdutoDAO.listar_por_preco(preco_min=menor_preco, preco_max=maior_preco)


    @staticmethod
    def obter(id_produto):
        """
        Retorna um único produto com base no ID.
        """
        return ProdutoDAO.obter_por_id(id_produto)

    @staticmethod
    def obter_por_lista(lista_id_produtos):
        """
        Retorna uma lista de produtos com base nos IDs.
        """
        return ProdutoDAO.obter_por_lista_id(lista_id_produtos)

    @staticmethod
    def criar(nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentarios):
        """
        Cria um novo produto.
        """

        fotos=fotos if fotos else ''
        rate=rate if rate else ''
        descricao=descricao if descricao else ''
        detalhes=detalhes if detalhes else ''
        comentarios=comentarios if comentarios else ''

        return ProdutoDAO.adicionar(nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentarios)

    @staticmethod
    def editar(id_produto, nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentarios):
        """
        Atualiza um produto existente.
        """
        produtoDB = ProdutoDAO.obter_por_id(id_produto)

        if not nome:
            nome = produtoDB.nome
        if not preco:
            preco = produtoDB.preco
        if not capa:
            capa = produtoDB.capa
        if not fotos:
            fotos = produtoDB.fotos
        if not estoque:
            estoque = produtoDB.estoque
        if not categoria:
            categoria = produtoDB.categoria
        if not rate:
            rate = produtoDB.rate
        if not descricao:
            descricao = produtoDB.descricao
        if not detalhes:
            detalhes = produtoDB.detalhes
        if not comentarios:
            comentarios = produtoDB.comentarios
        return ProdutoDAO.atualizar(id_produto, nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentarios)

    @staticmethod
    def remover(id_produto):
        """
        Elimina um produto da base de dados.
        """
        return ProdutoDAO.apagar(id_produto)
