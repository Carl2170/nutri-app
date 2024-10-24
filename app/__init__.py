from flask import Flask
from flasgger import Swagger

from app.routes.user import user_bp
from app.routes.health_profile import health_profile_bp
from app.routes.health_objective import health_objective_bp
from app.extensions import ma
from app.routes.auth import auth_bp
from app.database import create_database, configure_app

def create_app():
    """Crea y configura la aplicación Flask.

    Returns:
        app: Instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__)
    swagger = Swagger(app)

    create_database()  # Crear la base de datos si no existe
    configure_app(app)  # Configura la aplicación con la base de datos
    #ma.init_app(app)  # Inicializa la extensión Marshmallow
    app.register_blueprint(auth_bp) 
    app.register_blueprint(user_bp)  # Registra el blueprint de usuarios
    app.register_blueprint(health_profile_bp) # Registra el blueprint de autenticación
    app.register_blueprint(health_objective_bp) # Registra el blueprint de autenticación
    return app
