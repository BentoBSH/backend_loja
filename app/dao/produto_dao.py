# backend_flask/app/dao/produto_dao.py

# Importa o modelo ORM
from app.models.produto_model import Produto
from app import db

# Classe DAO com métodos de acesso à base de dados
class ProdutoDAO:

    @staticmethod
    def listar_todos():
        """
        Devolve todos os produtoes da base de dados.
        """
        return Produto.query.all()

    @staticmethod
    def listar_todos_com_offset_limit(offset, limit):
        """
        Devolve todos os produtos da base de dados com offset e limit.
        """
        # Função para listar produtos com offset e limit
        produtos = Produto.query.offset(offset).limit(limit).all()
        return produtos
    
    @staticmethod
    def listar_por_preco(preco_min, preco_max):
        """
        Devolve os produtos da base de dados numa range de preços.
        """
        produto = Produto.query.filter(Produto.preco.between(preco_min, preco_max)).all()
        return produto
    
    @staticmethod
    def listar_por_categoria(categoria_busca):
        """
        Devolve todos os produtos da base de dados que tenham nome semelhante ao recebido.
        """
        produtos = Produto.query.filter(Produto.categoria.ilike(f"%{categoria_busca}%")).all()
        return produtos


    @staticmethod
    def listar_por_nome(nome_busca):
        """
        Devolve todos os produtos da base de dados que tenham nome semelhante ao recebido.
        """
        produtos = Produto.query.filter(Produto.nome.ilike(f"%{nome_busca}%")).all()
        return produtos

    @staticmethod
    def obter_por_id(id_produto):
        """
        Devolve um produto com base no ID.
        """
        return Produto.query.get(id_produto)

    @staticmethod
    def obter_por_lista_id(lista_ids):
        """
        Devolve um produto com base no ID.
        """
        return [Produto.query.get(id_produto) for id_produto in lista_ids ] 

    @staticmethod
    def adicionar(nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentarios):
        """ 
        Adiciona um novo produto à base de dados.
        """ 
        novo = Produto(nome=nome, preco=preco, capa=capa, fotos=fotos, estoque=estoque, categoria=categoria, rate=rate, descricao=descricao, detalhes=detalhes, comentarios=comentarios)
        db.session.add(novo) 
        db.session.commit() 
        return novo 

    @staticmethod
    def atualizar(id_produto, nome, preco, capa, fotos, estoque, categoria, rate, descricao, detalhes, comentarios):
        """
        Atualiza um produto existente.
        """
        produto = Produto.query.get(id_produto)
        if produto:
            produto.nome = nome
            produto.preco = preco
            produto.capa = capa
            produto.fotos = fotos
            produto.estoque = estoque
            produto.categoria = categoria
            produto.rate = rate
            produto.descricao = descricao
            produto.detalhes = detalhes
            produto.comentarios = comentarios
            db.session.add(produto)
            db.session.commit()
        return produto

    @staticmethod
    def apagar(id_produto):
        """
        Remove um produto da base de dados.
        """
        produto = Produto.query.get(id_produto)
        if produto:
            db.session.delete(produto)
            db.session.commit()
            return True
        return False
