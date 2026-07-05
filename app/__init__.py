# app/__init__.py
from flask import Flask, redirect, url_for
import pymysql
import os
from dotenv import load_dotenv
from dbutils.pooled_db import PooledDB # Asegúrate de instalar: pip install DBUtils

# Cargar variables del archivo .env
load_dotenv()

# --- CONFIGURACIÓN DEL POOL DE CONEXIONES ---
# Esto reemplaza tu conexión simple por un contenedor de conexiones reutilizables
db_pool = PooledDB(
    creator=pymysql,
    maxconnections=30,  # Máximo de conexiones simultáneas
    mincached=5,        # Conexiones mínimas siempre listas
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'unemi_concierto_v2'),
    cursorclass=pymysql.cursors.DictCursor
)

def get_db_connection():
    """Retorna una conexión desde el pool en lugar de crear una nueva."""
    return db_pool.connection()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_secreta_default')

    # --- REGISTRO DE BLUEPRINTS ---
    from app.views.auth import auth_bp
    from app.views.user_dashboard import user_bp
    from app.controllers.reservas_api import reservas_bp
    from app.controllers.pagos_api import pagos_bp
    from app.controllers.admin_api import admin_bp
    from app.controllers.eventos_api import admin_eventos_bp
    from app.controllers.usuarios_api import admin_usuarios_bp
    from app.controllers.asientos_api import admin_asientos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_eventos_bp)
    app.register_blueprint(admin_usuarios_bp)
    app.register_blueprint(admin_asientos_bp)

    @app.route('/login')
    def login_alias():
        return redirect(url_for('auth.login_page'))

    return app