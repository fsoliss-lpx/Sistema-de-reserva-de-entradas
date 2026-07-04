# app/views/user_dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from app.models.evento_model import EventoModel
from app.models.asiento_model import AsientoModel

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
@user_bp.route('/evento/<int:id_evento>/asientos')
def mapa_asientos(id_evento):
    # Protegemos la ruta
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
        
    asientos = AsientoModel.obtener_asientos_por_evento(id_evento)
    
    return render_template('usuario/mapa_asientos.html', asientos=asientos, id_evento=id_evento)