from flask import Flask
import pymysql
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def get_db_connection():
    """Establece y retorna la conexión a la base de datos."""
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'unemi_concierto_v2'),
        cursorclass=pymysql.cursors.DictCursor
    )

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_secreta_default')

    # Aquí registraremos los Blueprints (Rutas)
    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app