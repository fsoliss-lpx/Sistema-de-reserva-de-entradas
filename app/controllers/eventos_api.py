# app/controllers/eventos_api.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.evento_model import EventoModel
from app.models.asiento_model import AsientoModel

admin_eventos_bp = Blueprint('admin_eventos', __name__, url_prefix='/admin/eventos')

@admin_eventos_bp.route('/')
def gestion_eventos():
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    eventos = EventoModel.obtener_todos_eventos()
    return render_template('admin/eventos.html', eventos=eventos)

@admin_eventos_bp.route('/nuevo')
def nuevo_evento():
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    return render_template('admin/evento_form.html', evento=None)

@admin_eventos_bp.route('/editar/<int:id_evento>')
def editar_evento(id_evento):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    evento = EventoModel.obtener_evento_por_id(id_evento)
    if not evento:
        flash('Evento no encontrado.', 'danger')
        return redirect(url_for('admin_eventos.gestion_eventos'))
    # obtener cantidad actual de asientos para prefijar en el formulario
    asientos = AsientoModel.obtener_asientos_por_evento(id_evento)
    cantidad_actual = len(asientos) if asientos is not None else 0
    return render_template('admin/evento_form.html', evento=evento, cantidad_asientos=cantidad_actual)

@admin_eventos_bp.route('/guardar', methods=['POST'])
@admin_eventos_bp.route('/guardar/<int:id_evento>', methods=['POST'])
def guardar_evento(id_evento=None):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    nombre_evento = request.form.get('nombre_evento')
    lugar = request.form.get('lugar')
    fecha_hora = request.form.get('fecha_hora')
    precio_base = request.form.get('precio_base')
    imagen_url = request.form.get('imagen_url')
    estado = request.form.get('estado', 'ACTIVO')

    if fecha_hora and 'T' in fecha_hora:
        fecha_hora = fecha_hora.replace('T', ' ')

    # Helper: genera etiquetas de asientos (A1, A2 ...)
    def row_label(n):
        # 0 -> A, 25 -> Z, 26 -> AA, etc.
        s = ''
        while n >= 0:
            s = chr(ord('A') + (n % 26)) + s
            n = n // 26 - 1
        return s

    def generate_labels(total, per_row):
        labels = []
        if per_row <= 0:
            per_row = 5
        rows = (total + per_row - 1) // per_row
        for r in range(rows):
            prefix = row_label(r)
            for c in range(1, per_row + 1):
                labels.append(f"{prefix}{c}")
                if len(labels) >= total:
                    break
            if len(labels) >= total:
                break
        return labels

    if id_evento:
        EventoModel.actualizar_evento(id_evento, nombre_evento, lugar, fecha_hora, precio_base, imagen_url, estado)
        # ajustar cantidad de asientos si se proporcionó
        try:
            cantidad = request.form.get('cantidad_asientos', None)
            if cantidad is not None:
                cantidad = int(cantidad or 0)
            else:
                cantidad = None
            per_row = request.form.get('asientos_por_fila', None)
            if per_row is not None:
                per_row = int(per_row or 5)
            else:
                per_row = 5
        except ValueError:
            cantidad = None
            per_row = 5

        if cantidad is not None:
            asientos_actuales = AsientoModel.obtener_asientos_por_evento(id_evento) or []
            existing_labels = [a.get('numero_asiento') for a in asientos_actuales]
            desired = generate_labels(cantidad, per_row)
            cuenta_actual = len(existing_labels)
            if cantidad > cuenta_actual:
                # crear asientos adicionales con etiquetas
                for label in desired[cuenta_actual:]:
                    AsientoModel.crear_asiento(id_evento, label, 'DISPONIBLE', 1)
            elif cantidad < cuenta_actual:
                # eliminar asientos sobrantes (los últimos en orden) si están DISPONIBLE
                to_remove = existing_labels[cantidad:]
                no_eliminados = []
                # map labels to records
                label_map = {a.get('numero_asiento'): a for a in asientos_actuales}
                for lab in reversed(to_remove):
                    rec = label_map.get(lab)
                    if not rec:
                        continue
                    if rec.get('estado') == 'DISPONIBLE':
                        AsientoModel.eliminar_asiento(rec.get('id_asiento'))
                    else:
                        no_eliminados.append(lab)
                if no_eliminados:
                    flash(f'No se pudieron eliminar los asientos: {no_eliminados} porque no están libres.', 'warning')

        flash('Evento actualizado correctamente.', 'success')
    else:
        nuevo_id = EventoModel.crear_evento(nombre_evento, lugar, fecha_hora, precio_base, imagen_url, estado)
        if nuevo_id:
            # Si el administrador indicó una cantidad de asientos, crearlos
            try:
                cantidad = int(request.form.get('cantidad_asientos', 0) or 0)
            except ValueError:
                cantidad = 0
            try:
                per_row = int(request.form.get('asientos_por_fila', 5) or 5)
            except ValueError:
                per_row = 5

            if cantidad > 0:
                labels = generate_labels(cantidad, per_row)
                for lab in labels:
                    AsientoModel.crear_asiento(nuevo_id, lab, 'DISPONIBLE', 1)

        flash('Evento creado correctamente.', 'success')

    return redirect(url_for('admin_eventos.gestion_eventos'))

@admin_eventos_bp.route('/eliminar/<int:id_evento>')
def eliminar_evento(id_evento):
    if session.get('rol') != 'ADMINISTRADOR':
        flash('Acceso denegado: No tienes permisos de administrador.', 'danger')
        return redirect(url_for('user.inicio'))

    # Verificar asientos asociados para evitar errores de FK en la DB
    asientos = AsientoModel.obtener_asientos_por_evento(id_evento) or []
    # Si existen asientos no disponibles, impedimos la eliminación
    no_eliminables = [a.get('numero_asiento') for a in asientos if a.get('estado') != 'DISPONIBLE']
    if no_eliminables:
        flash(f'No se puede eliminar el evento porque existen asientos ocupados/no disponibles: {no_eliminables}', 'warning')
        return redirect(url_for('admin_eventos.gestion_eventos'))

    # Borrar asientos disponibles primero, luego el evento
    try:
        for a in asientos:
            AsientoModel.eliminar_asiento(a.get('id_asiento'))
    except Exception:
        flash('Error al eliminar asientos asociados. Intenta nuevamente.', 'danger')
        return redirect(url_for('admin_eventos.gestion_eventos'))

    # Finalmente eliminar el evento
    success = EventoModel.eliminar_evento(id_evento)
    if success:
        flash('Evento eliminado correctamente.', 'success')
    else:
        flash('Error al eliminar el evento. Revisa los logs.', 'danger')
    return redirect(url_for('admin_eventos.gestion_eventos'))
