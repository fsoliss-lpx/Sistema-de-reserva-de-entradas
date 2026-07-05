# app/controllers/admin_api.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.admin_model import AdminModel

# Solo definimos el blueprint una vez
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard_admin():
    # Validación de seguridad estricta
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        # Redirigimos usando url_for para mayor seguridad
        return redirect(url_for('user.inicio')) 
        
    # Si pasa la validación, obtenemos el reporte y mostramos la vista
    reporte = AdminModel.obtener_reporte_ventas()
    return render_template('admin/dashboard_admin.html', reporte=reporte)