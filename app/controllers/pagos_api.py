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

    resultado = request.form.get('resultado', 'exito') # Por defecto éxito si el form falla
    simulacion_exitosa = True if resultado == 'exito' else False

    # 🛡️ BLINDAJE DE SEGURIDAD: Obtenemos el precio directamente de la BD 
    # para asegurar que MySQL no haga Rollback por recibir un monto vacío (None)
    conexion = get_db_connection()
    monto_seguro = 0.00
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT e.precio_base 
                FROM reservas r
                JOIN asientos a ON r.id_asiento = a.id_asiento
                JOIN eventos e ON a.id_evento = e.id_evento
                WHERE r.id_reserva = %s
            """, (id_reserva,))
            evento_data = cursor.fetchone()
            if evento_data:
                monto_seguro = float(evento_data['precio_base'])
    finally:
        conexion.close()

    # Ejecutamos la transacción ACID con el monto seguro
    exito, mensaje = PagoModel.procesar_pago(id_reserva, session['usuario_id'], simulacion_exitosa, monto_seguro)

    if exito and simulacion_exitosa:
        # REDIRECCIÓN CORREGIDA: Va al comprobante
        return redirect(url_for('pagos_api.ver_comprobante', id_reserva=id_reserva))
    else:
        flash(mensaje, 'danger')
        return redirect('/dashboard')

# NUEVA RUTA: Generar el comprobante visual
@pagos_bp.route('/comprobante/<int:id_reserva>', methods=['GET'])
def ver_comprobante(id_reserva):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    conexion = get_db_connection()
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT r.id_reserva, a.numero_asiento, e.nombre_evento, e.lugar, p.monto, p.fecha_pago, u.nombre_completo
                FROM reservas r
                JOIN asientos a ON r.id_asiento = a.id_asiento
                JOIN eventos e ON a.id_evento = e.id_evento
                JOIN pagos p ON r.id_reserva = p.id_reserva
                JOIN usuarios u ON r.id_usuario = u.id_usuario
                WHERE r.id_reserva = %s AND r.id_usuario = %s AND r.estado = 'CONFIRMADA'
            """
            cursor.execute(sql, (id_reserva, session['usuario_id']))
            comprobante_data = cursor.fetchone()

            if not comprobante_data:
                return redirect('/dashboard')

            return render_template('usuario/comprobante.html', comprobante=comprobante_data)
    finally:
        conexion.close()
    