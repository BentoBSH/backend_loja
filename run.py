# backend_flask/run.py

# Importa a função de criação da app
from app import criar_app

# Cria a app usando a função definida em __init__.py
app = criar_app()

# Executa a aplicação
if __name__ == "__main__":
    app.run(debug=False, port=4000) 
