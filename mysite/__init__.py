import os
from flask import Flask
from . import db, auth

def create_app(test_config = None):
    
    # Instancia de la clase Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # config db
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'biblioteca.sqlite'),
    )

    db.init_app(app)
    app.register_blueprint(auth.bp)
    
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