# app/models/admin_model.py
from app import get_db_connection

class AdminModel:
    @staticmethod
    def obtener_reporte_ventas():
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # Obtenemos un resumen de ventas por evento
                sql = """
                    SELECT e.nombre_evento, 
                           COUNT(r.id_reserva) as total_reservas,
                           SUM(p.monto) as recaudacion_total
                    FROM eventos e
                    LEFT JOIN asientos a ON e.id_evento = a.id_evento
                    LEFT JOIN reservas r ON a.id_asiento = r.id_asiento
                    LEFT JOIN pagos p ON r.id_reserva = p.id_reserva AND p.estado = 'EXITOSO'
                    GROUP BY e.id_evento
                """
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conexion.close()