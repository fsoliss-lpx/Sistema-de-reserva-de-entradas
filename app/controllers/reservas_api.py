# app/controllers/reservas_api.py
from flask import Blueprint, request, jsonify, session
from app.models.reserva_model import ReservaModel
from app.models.asiento_model import AsientoModel 

# Definimos el blueprint con el prefijo correcto
reservas_bp = Blueprint('reservas_api', __name__, url_prefix='/api/reservar')

@reservas_bp.route('/', methods=['POST'])
def reservar_asiento():
    
    print(f"DEBUG: Petición recibida. Sesión actual: {session.get('usuario_id')}")
    # 1. Validación de sesión
    if 'usuario_id' not in session:
        return jsonify({'status': 'error', 'message': 'No autenticado'}), 401
        
    # 2. Obtención de datos
    data = request.get_json()
    if not data or 'id_asiento' not in data:
        return jsonify({'status': 'error', 'message': 'Datos inválidos'}), 400
        
    id_asiento = data.get('id_asiento')
    
    # 3. Verificación de asiento
    asiento = AsientoModel.obtener_por_id(id_asiento)
    if not asiento:
        return jsonify({'status': 'error', 'message': 'Asiento no encontrado'}), 404
        
    if asiento['estado'] != 'DISPONIBLE':
        return jsonify({'status': 'error', 'message': 'El asiento ya no está disponible'}), 409

    # 4. Bloqueo optimista (Transacción segura)
    id_nueva_reserva = ReservaModel.intentar_reservar(id_asiento, session['usuario_id'], asiento['version'])
    
    if id_nueva_reserva:
        return jsonify({
            'status': 'success', 
            'message': '¡Asiento bloqueado temporalmente por 10 minutos!',
            'id_reserva': id_nueva_reserva
        }), 200
    else:
        return jsonify({
            'status': 'error', 
            'message': '¡Condición de Carrera! Otro usuario acaba de tomar este asiento.'
        }), 409