# backend_flask/app/dao/utilizador_dao.py

# Importa o modelo ORM
from app.models.utilizador_model import Utilizador
from app.models.endereco_model import Endereco
from app.models.carrinho_model import Carrinho
from app import db

# Classe DAO com métodos de acesso à base de dados
class UtilizadorDAO:

    @staticmethod
    def listar_todos():
        """
        Devolve todos os utilizadores da base de dados.
        """
        return Utilizador.query.all()

    @staticmethod
    def obter_por_id(id_utilizador):
        """
        Devolve um utilizador com base no ID.
        """
        return Utilizador.query.filter_by(id=id_utilizador).first()
    
    @staticmethod
    def obter_por_email(email_utilizador):
        """
        Devolve um utilizador com base no ID.
        """
        return Utilizador.query.filter_by(email=email_utilizador).all()

    @staticmethod
    def adicionar(nome, email, grupo, palavra_passe):
        """
        Adiciona um novo utilizador à base de dados.
        """
        novo = Utilizador(nome=nome, email=email, grupo=grupo, palavra_passe=palavra_passe)
        db.session.add(novo)
        db.session.commit()
        return novo
    
    
    @staticmethod
    def adicionar_ao_carrinho(id_utilizador, id_produto, quantidade):
        """
        Adiciona produto ao carrinho de um utilizador.
        """
        # verifica se o item já existe antes de ser adicionado e caso exista incrementa a quantidade
        item_na_db = Carrinho.query.filter_by(id_utilizador=id_utilizador, id_produto=id_produto).first()
        if item_na_db:
            item_na_db.quantidade = item_na_db.quantidade + quantidade
            db.session.add(item_na_db)
            db.session.commit()
            return item_na_db
        
        item_carrinho = Carrinho(id_utilizador=id_utilizador, id_produto=id_produto, quantidade=quantidade)
        db.session.add(item_carrinho)
        db.session.commit()
        return item_carrinho

    @staticmethod
    def atualizar_carrinho(id_utilizador, id_produto, nova_quantidade):
        """
        Remove um produto da base de dados.
        """
        item = Carrinho.query.filter_by(id_utilizador=id_utilizador, id_produto=id_produto).first()

        if item:
            item.quantidade = nova_quantidade
            db.session.add(item)
            db.session.commit()
            return item

    @staticmethod
    def atualizar(id_utilizador, nome, email, grupo, palavra_passe):
        """
        Atualiza um utilizador existente.
        """
        utilizador = Utilizador.query.get(id_utilizador)
        if utilizador:
            utilizador.nome = nome
            utilizador.email = email
            utilizador.grupo = grupo
            utilizador.palavra_passe = palavra_passe
            db.session.add(utilizador)
            db.session.commit()
        return utilizador

    @staticmethod
    def apagar(id_utilizador):
        """
        Remove um utilizador da base de dados.
        """
        utilizador = Utilizador.query.get(id_utilizador)
        if utilizador:
            db.session.delete(utilizador)
            db.session.commit()
            return True
        
    @staticmethod
    def remover_p_do_carrinho(id_utilizador, id_produto):
        """
        Remove um produto da base de dados.
        """
        item = Carrinho.query.filter_by(id_utilizador=id_utilizador, id_produto=id_produto).first()

        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def obter_endereco(id):
        """
        Devolve um utilizador com base no ID.
        """
        endereco = Endereco.query.filter_by(id_utilizador=id).first()
        if endereco:
            return endereco
        return 

    @staticmethod
    def atualizar_endereco(id, email, telefone, municipio, detalhes_rua):
        """
        Atualiza um utilizador existente.
        """
        novo_endereco = Endereco.query.get(id)

        if novo_endereco:
            nome = novo_endereco.utilizadores.nome
            novo_endereco.id_utilizador = id
            novo_endereco.email = email
            novo_endereco.telefone = telefone
            novo_endereco.municipio = municipio
            novo_endereco.detalhes_rua = detalhes_rua
            db.session.add(novo_endereco)
            db.session.commit()
            novo_endereco.nome = nome
            return novo_endereco
        else:
            utilizador = Utilizador.query.get(id)
            endereco = Endereco(id, email, telefone, municipio, detalhes_rua)
            db.session.add(endereco)
            db.session.commit()
            endereco.nome = utilizador.nome
            return endereco
    
