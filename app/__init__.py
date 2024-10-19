from flask import Flask
from app.routes.usuarios import usuarios_bp
from app.database import create_database, configure_app, db

def create_app():
    """Crea y configura la aplicación Flask.

    Returns:
        app: Instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__)

    create_database()  # Crear la base de datos si no existe
    configure_app(app)  # Configura la aplicación con la base de datos

    app.register_blueprint(usuarios_bp)  # Registra el blueprint de usuarios
    return app
