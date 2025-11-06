# backend_flask/run.py

# Importa a função de criação da app
from app import criar_app

# Cria a app usando a função definida em __init__.py
app, socketio = criar_app()

# Executa a aplicação
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=4000)
