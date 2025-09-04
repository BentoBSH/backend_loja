# backend_flask/app/__init__.py

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from config import Config  # Caminho correto se usares 'run.py' dentro de backend_flask/
from flask_cors import CORS


# Inicializa o ORM
db = SQLAlchemy()

def criar_app():
    # Criação da app Flask com caminhos externos para HTML e CSS

    app = Flask(__name__,
                template_folder="../frontend_html/templates",
                static_folder="../frontend_html/static")

    # Carrega as configurações a partir da classe Config
    app.config.from_object(Config)

    # Inicializa a ligação à base de dados
    db.init_app(app)

    # importa socketio
    from app.sockets import socketio
    socketio.init_app(app)

    with app.app_context():
        # Registo dos blueprints
        from app.api.utilizadores_api import utilizadores
        from app.api.produto_api import produtos
        from app.web.web_view import web
        from app.api.email_api import webmail
        from app.services.stripe import stripeBlueprint
        from app.routes.chat_routes import chat_bp

        app.register_blueprint(utilizadores)
        app.register_blueprint(web)
        app.register_blueprint(produtos)
        app.register_blueprint(webmail)
        app.register_blueprint(stripeBlueprint)
        app.register_blueprint(chat_bp)



        # Rota para servir o ficheiro swagger.yaml a partir da pasta /docs
        @app.route("/swagger.yaml")
        def swagger_spec():
            return send_from_directory("../docs", "swagger.yaml")

        # Swagger UI Blueprint            
        swaggerui_blueprint = get_swaggerui_blueprint(
            '/apidocs',
            '/swagger.yaml',  # Agora usa a rota personalizada acima
            config={ 'app_name': "Rotas de produtos Flask" },
            oauth_config={}
        )
        app.register_blueprint(swaggerui_blueprint, url_prefix='/apidocs')

        # Criação automática das tabelas (se ainda não existirem)
        CORS(app)
        db.create_all()

    return app, socketio
