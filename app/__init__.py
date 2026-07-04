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

    # --- AQUÍ ESTÁ LA CLAVE PARA QUE NO SALGA 404 ---
    
    # 1. Registrar las rutas de Autenticación (Login y Registro)
    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp)

    # 2. Registrar las rutas del Dashboard del Usuario
    from app.views.user_dashboard import user_bp
    app.register_blueprint(user_bp)

    # Registrar la API de Reservas
    from app.controllers.reservas_api import reservas_bp
    app.register_blueprint(reservas_bp)

    return app
