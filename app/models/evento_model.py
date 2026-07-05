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

    @staticmethod
    def obtener_todos_eventos():
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM eventos ORDER BY fecha_hora ASC"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener todos los eventos: {e}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def obtener_evento_por_id(id_evento):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM eventos WHERE id_evento = %s"
                cursor.execute(sql, (id_evento,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener evento por id: {e}")
            return None
        finally:
            conexion.close()

    @staticmethod
    def crear_evento(nombre_evento, lugar, fecha_hora, precio_base, imagen_url, estado):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = """INSERT INTO eventos (nombre_evento, lugar, fecha_hora, precio_base, imagen_url, estado)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (nombre_evento, lugar, fecha_hora, precio_base, imagen_url, estado))
                nuevo_id = cursor.lastrowid
            conexion.commit()
            return nuevo_id
        except Exception as e:
            print(f"Error al crear evento: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def actualizar_evento(id_evento, nombre_evento, lugar, fecha_hora, precio_base, imagen_url, estado):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = """UPDATE eventos SET nombre_evento = %s, lugar = %s, fecha_hora = %s, precio_base = %s,
                         imagen_url = %s, estado = %s WHERE id_evento = %s"""
                cursor.execute(sql, (nombre_evento, lugar, fecha_hora, precio_base, imagen_url, estado, id_evento))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar evento: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def eliminar_evento(id_evento):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "DELETE FROM eventos WHERE id_evento = %s"
                cursor.execute(sql, (id_evento,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar evento: {e}")
            return False
        finally:
            conexion.close()