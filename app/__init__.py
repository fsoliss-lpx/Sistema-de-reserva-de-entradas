from flask import Flask, redirect, url_for
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

    # --- REGISTRO DE BLUEPRINTS ---
    
    # 1. Autenticación
    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp)

    # 2. Usuario
    from app.views.user_dashboard import user_bp
    app.register_blueprint(user_bp)

    # 3. Reservas
    from app.controllers.reservas_api import reservas_bp
    app.register_blueprint(reservas_bp)

    # 4. Pagos
    from app.controllers.pagos_api import pagos_bp
    app.register_blueprint(pagos_bp)

    # 5. Administración (Sprint 8)
    from app.controllers.admin_api import admin_bp
    app.register_blueprint(admin_bp)

    # 6. Administración de Eventos
    from app.controllers.eventos_api import admin_eventos_bp
    app.register_blueprint(admin_eventos_bp)

    # 7. Administración de Usuarios
    from app.controllers.usuarios_api import admin_usuarios_bp
    app.register_blueprint(admin_usuarios_bp)

    # 8. Administración de Asientos
    from app.controllers.asientos_api import admin_asientos_bp
    app.register_blueprint(admin_asientos_bp)

    # Ruta alternativa para /login -> /auth/login ->
    @app.route('/login')
    def login_alias():
        return redirect(url_for('auth.login_page'))

    return app