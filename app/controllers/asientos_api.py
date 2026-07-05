# app/controllers/asientos_api.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.asiento_model import AsientoModel
from app.models.evento_model import EventoModel

admin_asientos_bp = Blueprint('admin_asientos', __name__, url_prefix='/admin/asientos')

@admin_asientos_bp.route('/')
def gestion_asientos():
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    asientos = AsientoModel.obtener_todos_asientos()
    return render_template('admin/asientos.html', asientos=asientos)

@admin_asientos_bp.route('/nuevo')
def nuevo_asiento():
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    eventos = EventoModel.obtener_todos_eventos()
    return render_template('admin/asiento_form.html', asiento=None, eventos=eventos)

@admin_asientos_bp.route('/editar/<int:id_asiento>')
def editar_asiento(id_asiento):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    asiento = AsientoModel.obtener_por_id(id_asiento)
    eventos = EventoModel.obtener_todos_eventos()
    if not asiento:
        flash('Asiento no encontrado.', 'danger')
        return redirect(url_for('admin_asientos.gestion_asientos'))
    return render_template('admin/asiento_form.html', asiento=asiento, eventos=eventos)

@admin_asientos_bp.route('/guardar', methods=['POST'])
@admin_asientos_bp.route('/guardar/<int:id_asiento>', methods=['POST'])
def guardar_asiento(id_asiento=None):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    id_evento = request.form.get('id_evento')
    numero_asiento = request.form.get('numero_asiento')
    estado = request.form.get('estado', 'DISPONIBLE')
    version = request.form.get('version', 1)

    if id_asiento:
        AsientoModel.actualizar_asiento(id_asiento, id_evento, numero_asiento, estado, version)
        flash('Asiento actualizado correctamente.', 'success')
    else:
        AsientoModel.crear_asiento(id_evento, numero_asiento, estado, version)
        flash('Asiento creado correctamente.', 'success')

    return redirect(url_for('admin_asientos.gestion_asientos'))

@admin_asientos_bp.route('/eliminar/<int:id_asiento>')
def eliminar_asiento(id_asiento):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    AsientoModel.eliminar_asiento(id_asiento)
    flash('Asiento eliminado correctamente.', 'success')
    return redirect(url_for('admin_asientos.gestion_asientos'))
