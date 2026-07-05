# app/controllers/usuarios_api.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario_model import UsuarioModel

admin_usuarios_bp = Blueprint('admin_usuarios', __name__, url_prefix='/admin/usuarios')

@admin_usuarios_bp.route('/')
def gestion_usuarios():
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    usuarios = UsuarioModel.obtener_usuarios()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_usuarios_bp.route('/editar/<int:id_usuario>')
def editar_usuario(id_usuario):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    usuario = UsuarioModel.obtener_usuario_por_id(id_usuario)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('admin_usuarios.gestion_usuarios'))
    return render_template('admin/editar_usuario.html', usuario=usuario)

@admin_usuarios_bp.route('/eliminar/<int:id_usuario>')
def eliminar_usuario(id_usuario):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    UsuarioModel.eliminar_usuario(id_usuario)
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('admin_usuarios.gestion_usuarios'))

@admin_usuarios_bp.route('/actualizar/<int:id_usuario>', methods=['POST'])
def actualizar_usuario(id_usuario):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    nombre_completo = request.form.get('nombre_completo')
    correo_electronico = request.form.get('correo_electronico')
    rol = request.form.get('rol')

    UsuarioModel.actualizar_usuario(id_usuario, nombre_completo, correo_electronico, rol)
    flash('Usuario actualizado correctamente.', 'success')
    return redirect(url_for('admin_usuarios.gestion_usuarios'))
