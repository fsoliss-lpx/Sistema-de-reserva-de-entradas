# app/controllers/pagos_api.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.pago_model import PagoModel
from app import get_db_connection

pagos_bp = Blueprint('pagos_api', __name__, url_prefix='/pago')

@pagos_bp.route('/<int:id_reserva>', methods=['GET'])
def vista_pago(id_reserva):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    conexion = get_db_connection()
    try:
        with conexion.cursor() as cursor:
            # Traer los datos cruzados para el resumen visual
            sql = """
                SELECT r.id_reserva, r.timestamp_expiracion, a.numero_asiento, e.nombre_evento, e.precio_base
                FROM reservas r
                JOIN asientos a ON r.id_asiento = a.id_asiento
                JOIN eventos e ON a.id_evento = e.id_evento
                WHERE r.id_reserva = %s AND r.id_usuario = %s AND r.estado = 'TEMPORAL'
            """
            cursor.execute(sql, (id_reserva, session['usuario_id']))
            detalle = cursor.fetchone()

            if not detalle:
                flash('La reserva expiró o no existe.', 'danger')
                return redirect('/dashboard')

            return render_template('usuario/pago.html', detalle=detalle)
    finally:
        conexion.close()

@pagos_bp.route('/<int:id_reserva>/procesar', methods=['POST'])
def procesar(id_reserva):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    resultado = request.form.get('resultado')
    monto = request.form.get('monto')
    simulacion_exitosa = True if resultado == 'exito' else False

    exito, mensaje = PagoModel.procesar_pago(id_reserva, session['usuario_id'], simulacion_exitosa, monto)

    if exito and simulacion_exitosa:
        flash(mensaje, 'success')
        return redirect('/dashboard')
    else:
        flash(mensaje, 'danger')
        return redirect('/dashboard')
    