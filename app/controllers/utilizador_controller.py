# backend_flask/app/controllers/utilizador_controller.py

# Importa a camada DAO
from app.dao.utilizador_dao import UtilizadorDAO

from argon2 import PasswordHasher

ph = PasswordHasher()

# Define a classe de controlo da lógica de negócio
class UtilizadorController:

    @staticmethod
    def listar():
        """
        Retorna todos os utilizadores.
        """
        return UtilizadorDAO.listar_todos()

    @staticmethod
    def obter(id_utilizador):
        """
        Retorna um único utilizador com base no ID.
        """
        return UtilizadorDAO.obter_por_id(id_utilizador)

    @staticmethod
    def adicionar_no_carrinho(id_utilizador, id_produto, quantidade):
        """
        Retorna o produto adicionado ao carrinho pelo utilizador.
        """
        return  UtilizadorDAO.adicionar_ao_carrinho(id_utilizador=id_utilizador, id_produto=id_produto, quantidade=quantidade)

    @staticmethod
    def atualizar_carrinho(id_utilizador, id_produto, nova_quantidade):
        """
        Retorna o produto adicionado ao carrinho pelo utilizador.
        """
        return  UtilizadorDAO.atualizar_carrinho(id_utilizador=id_utilizador, id_produto=id_produto, nova_quantidade=nova_quantidade)

    @staticmethod
    def obter_via_email(email_utilizador):
        """
        Retorna um único utilizador com base no email.
        """
        return UtilizadorDAO.obter_por_email(email_utilizador)

    @staticmethod
    def criar(nome, email, grupo, palavra_passe):
        """
        Cria um novo utilizador.
        """
        return UtilizadorDAO.adicionar(nome, email, grupo, palavra_passe)

    @staticmethod
    def editar(id_utilizador, nome, email, grupo, palavra_passe):
        """
        Atualiza um utilizador existente.
        """
        usuarioDB = UtilizadorDAO.obter_por_id(id_utilizador)
        if usuarioDB:
            dadosAntigos = usuarioDB[0]
        if not nome:
            nome = dadosAntigos.nome
        if not email:
            email = dadosAntigos.email
        if not grupo:
            grupo = dadosAntigos.grupo
        if not palavra_passe:
            palavra_passe = dadosAntigos.palavra_passe
        else:
            password_hash = ph.hash(palavra_passe)
            palavra_passe = password_hash

        return UtilizadorDAO.atualizar(id_utilizador, nome, email, grupo, palavra_passe)

    @staticmethod
    def remover(id_utilizador):
        """
        Elimina um utilizador da base de dados.
        """
        return UtilizadorDAO.apagar(id_utilizador)
    
    @staticmethod
    def remover_do_carrinho(id_utilizador, id_produto):
        """
        Retorna o produto adicionado ao carrinho pelo utilizador.
        """
        return  UtilizadorDAO.remover_p_do_carrinho(id_utilizador=id_utilizador, id_produto=id_produto)
    
    @staticmethod
    def obter_endereco(id):
        """
        Retorna o endereço do utilizador.
        """
        endereco = UtilizadorDAO.obter_endereco(id)
        if endereco:
            nome = endereco.utilizador.nome
            endereco.nome = nome
            return  endereco
        return


    @staticmethod
    def atualizar_endereco(id, email, telefone, municipio, detalhes_rua):
        """
        Retorna o endereço atualizado.
        """
        return  UtilizadorDAO.atualizar_endereco(id, email, telefone, municipio, detalhes_rua)


    @staticmethod
    def adicionar_ao_historico(id_utilizador, id_produtos, quantidades, id_compra):
        """
        Retorna os produtos adicionados ao carrinho pelo utilizador.
        """
        return  UtilizadorDAO.adicionar_ao_historico(id_utilizador=id_utilizador, id_produtos=id_produtos, quantidades=quantidades, id_compra=id_compra)
