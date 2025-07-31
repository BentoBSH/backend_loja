# backend_flask/app/dao/utilizador_dao.py

# Importa o modelo ORM
from app.models.utilizador_model import Utilizador
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
        return Utilizador.query.filter_by(id=id_utilizador).all()
    
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
        return False
