# app/views/user_dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for

# Creamos el Blueprint con un prefijo para todas las rutas del usuario
user_bp = Blueprint('user', __name__, url_prefix='/dashboard')

@user_bp.route('/')
def inicio():
    # 1. Proteger la ruta: Si no hay sesión iniciada, lo pateamos al login
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    # 2. Seguridad extra: Si un Admin intenta entrar aquí, lo enviamos a su zona
    if session.get('rol') == 'ADMINISTRADOR':
        return redirect('/admin') # Ruta que crearemos en el Sprint 8

    # 3. Extraemos el nombre de la sesión para la bienvenida
    nombre_usuario = session.get('nombre', 'Usuario')
    
    return render_template('usuario/dashboard.html', nombre=nombre_usuario)