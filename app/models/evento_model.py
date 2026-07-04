# app/models/evento_model.py
from app import get_db_connection

class EventoModel:
    @staticmethod
    def obtener_eventos_activos():
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # Obtenemos solo los eventos que estén activos
                sql = "SELECT * FROM eventos WHERE estado = 'ACTIVO' ORDER BY fecha_hora ASC"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener eventos: {e}")
            return []
        finally:
            conexion.close()