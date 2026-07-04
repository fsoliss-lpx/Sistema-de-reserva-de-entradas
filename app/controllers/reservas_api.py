# app/controllers/reservas_api.py
from flask import Blueprint, request, jsonify, session
from app.models.reserva_model import ReservaModel
from app.models.asiento_model import AsientoModel 

reservas_bp = Blueprint('reservas_api', __name__, url_prefix='/api/reservar')

@reservas_bp.route('/', methods=['POST'])
def reservar_asiento():
    if 'usuario_id' not in session:
        return jsonify({'status': 'error', 'message': 'No autenticado'}), 401
        
    data = request.get_json()
    id_asiento = data.get('id_asiento')
    
    # Obtener estado y versión actual
    asiento = AsientoModel.obtener_por_id(id_asiento)
    if not asiento:
        return jsonify({'status': 'error', 'message': 'Asiento no encontrado'}), 404
        
    if asiento['estado'] != 'DISPONIBLE':
        return jsonify({'status': 'error', 'message': 'El asiento ya no está disponible'}), 409

    # Intentar ejecutar el bloqueo optimista en MySQL
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