from flask import Blueprint, render_template, session, redirect, url_for, request, flash # <-- Agregamos request y flash
from app.models.evento_model import EventoModel
from app.models.asiento_model import AsientoModel
from app.models.reserva_model import ReservaModel
from app.models.usuario_model import UsuarioModel

user_bp = Blueprint('user', __name__, url_prefix='/dashboard')

@user_bp.route('/')
def inicio():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('rol') == 'ADMINISTRADOR':
        return redirect('/admin') 

    nombre_usuario = session.get('nombre', 'Usuario')
    lista_eventos = EventoModel.obtener_eventos_activos()
    return render_template('usuario/dashboard.html', nombre=nombre_usuario, eventos=lista_eventos)

@user_bp.route('/evento/<int:id_evento>/asientos')
def mapa_asientos(id_evento):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    asientos = AsientoModel.obtener_asientos_por_evento(id_evento)
    return render_template('usuario/mapa_asientos.html', asientos=asientos, id_evento=id_evento)

@user_bp.route('/historial')
def historial():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    historial_compras = ReservaModel.obtener_historial_usuario(session['usuario_id'])
    return render_template('usuario/historial.html', nombre=session['nombre'], historial=historial_compras)

@user_bp.route('/comprobante/<int:id_reserva>')
def comprobante(id_reserva):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    compras = ReservaModel.obtener_historial_usuario(session['usuario_id'])
    ticket = next((compra for compra in compras if compra['id_reserva'] == id_reserva), None)
    
    if not ticket or ticket['estado_reserva'] != 'CONFIRMADA':
        flash('El comprobante no existe o la reserva no está confirmada.', 'danger')
        return redirect(url_for('user.historial'))
    return render_template('usuario/comprobante.html', ticket=ticket, nombre=session['nombre'])

@user_bp.route('/perfil/cambiar-password', methods=['POST'])
def cambiar_password():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
        
    actual = request.form.get('actual')
    nueva = request.form.get('nueva')
    
    exito, mensaje = UsuarioModel.actualizar_contrasena(session['usuario_id'], actual, nueva)
    
    if exito:
        flash(mensaje, 'success')
    else:
        flash(mensaje, 'danger')
        
    return redirect(url_for('user.perfil'))

@user_bp.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
        
    # Consultamos los datos actuales del usuario para mostrarlos en el perfil
    usuario = UsuarioModel.obtener_datos_usuario(session['usuario_id']) 
    return render_template('usuario/perfil.html', usuario=usuario)