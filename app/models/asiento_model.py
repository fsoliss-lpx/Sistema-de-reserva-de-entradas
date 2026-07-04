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
                sql = "SELECT * FROM asientos WHERE id_evento = %s ORDER BY numero_asiento"
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