import os
import sys
import traceback

# Asegurar que el directorio raíz del proyecto esté en sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import get_db_connection

try:
    conn = get_db_connection()
    print('Conexión exitosa')
    conn.close()
except Exception as e:
    traceback.print_exc()
    print('Error al conectar:', e)
