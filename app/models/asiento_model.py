import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'unemi_concierto_v2'),
        cursorclass=pymysql.cursors.DictCursor
    )

class AsientoModel:
    @staticmethod
    def obtener_asientos_por_evento(id_evento):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM asientos WHERE id_evento = %s ORDER BY REGEXP_REPLACE(numero_asiento, '[0-9]+', ''), CAST(REGEXP_SUBSTR(numero_asiento, '[0-9]+') AS UNSIGNED) ASC"
                cursor.execute(sql, (id_evento,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener asientos: {e}")
            return []
        finally:
            conexion.close()

    # --- AQUÍ ESTÁ LA NUEVA FUNCIÓN ---
    @staticmethod
    def obtener_por_id(id_asiento):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM asientos WHERE id_asiento = %s"
                cursor.execute(sql, (id_asiento,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener asiento por ID: {e}")
            return None
        finally:
            conexion.close()

    @staticmethod
    def obtener_todos_asientos():
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT a.*, e.nombre_evento FROM asientos a JOIN eventos e ON a.id_evento = e.id_evento ORDER BY e.fecha_hora, REGEXP_REPLACE(a.numero_asiento, '[0-9]+', ''), CAST(REGEXP_SUBSTR(a.numero_asiento, '[0-9]+') AS UNSIGNED) ASC"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener todos los asientos: {e}")
            return []
        finally:
            conexion.close()

    @staticmethod
    def crear_asiento(id_evento, numero_asiento, estado, version):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO asientos (id_evento, numero_asiento, estado, version) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (id_evento, numero_asiento, estado, version))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al crear asiento: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def actualizar_asiento(id_asiento, id_evento, numero_asiento, estado, version):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "UPDATE asientos SET id_evento = %s, numero_asiento = %s, estado = %s, version = %s WHERE id_asiento = %s"
                cursor.execute(sql, (id_evento, numero_asiento, estado, version, id_asiento))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar asiento: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def eliminar_asiento(id_asiento):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "DELETE FROM asientos WHERE id_asiento = %s"
                cursor.execute(sql, (id_asiento,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar asiento: {e}")
            return False
        finally:
            conexion.close()