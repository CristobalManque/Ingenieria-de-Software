import os
from flask import Flask

def create_app(test_config = None):
    
    # Instancia de la clase Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # config db (por añadir)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Pagina que retorna "Hola mundo"
    @app.route("/")
    def hola_mundo():
        return "Hola mundo"
    
    return app