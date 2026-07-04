# app/views/user_dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from app.models.evento_model import EventoModel

user_bp = Blueprint('user', __name__, url_prefix='/dashboard')

@user_bp.route('/')
def inicio():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('rol') == 'ADMINISTRADOR':
        return redirect('/admin') 

    nombre_usuario = session.get('nombre', 'Usuario')
    
    # NUEVO: Obtenemos los eventos desde la base de datos
    lista_eventos = EventoModel.obtener_eventos_activos()
    
    # Pasamos la variable 'eventos' a la vista HTML
    return render_template('usuario/dashboard.html', nombre=nombre_usuario, eventos=lista_eventos)