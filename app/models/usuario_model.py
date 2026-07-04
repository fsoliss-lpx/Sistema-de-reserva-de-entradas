from app import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:
    @staticmethod
    def registrar_usuario(nombre_completo, correo, contrasena):
        # Encriptar la contraseña
        hash_pass = generate_password_hash(contrasena)
        
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = """INSERT INTO usuarios (nombre_completo, correo_electronico, contrasena_hash) 
                         VALUES (%s, %s, %s)"""
                cursor.execute(sql, (nombre_completo, correo, hash_pass))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def verificar_login(correo, contrasena):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE correo_electronico = %s"
                cursor.execute(sql, (correo,))
                usuario = cursor.fetchone()
                
                # Verificar si el usuario existe y la contraseña coincide con el hash
                if usuario and check_password_hash(usuario['contrasena_hash'], contrasena):
                    return usuario
                return None
        finally:
            conexion.close()