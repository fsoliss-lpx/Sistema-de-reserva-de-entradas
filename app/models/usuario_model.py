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

    @staticmethod
    def actualizar_contrasena(id_usuario, contrasena_actual, nueva_contrasena):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # 1. Obtener el hash actual
                cursor.execute("SELECT contrasena_hash FROM usuarios WHERE id_usuario = %s", (id_usuario,))
                usuario = cursor.fetchone()
                
                # 2. Verificar que la contraseña actual sea correcta
                if usuario and check_password_hash(usuario['contrasena_hash'], contrasena_actual):
                    # 3. Hashear la nueva y actualizar
                    nuevo_hash = generate_password_hash(nueva_contrasena)
                    cursor.execute("UPDATE usuarios SET contrasena_hash = %s WHERE id_usuario = %s", 
                                   (nuevo_hash, id_usuario))
                    conexion.commit()
                    return True, "Contraseña actualizada exitosamente."
                return False, "La contraseña actual es incorrecta."
        except Exception as e:
            print(f"Error: {e}")
            return False, "Error al actualizar la contraseña."
        finally:
            conexion.close()

    @staticmethod
    def obtener_datos_usuario(id_usuario):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT nombre_completo, correo_electronico FROM usuarios WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def obtener_usuarios():
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT id_usuario, nombre_completo, correo_electronico, rol FROM usuarios"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT id_usuario, nombre_completo, correo_electronico, rol FROM usuarios WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def eliminar_usuario(id_usuario):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "DELETE FROM usuarios WHERE id_usuario = %s"
                cursor.execute(sql, (id_usuario,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
        finally:
            conexion.close()

    @staticmethod
    def actualizar_usuario(id_usuario, nombre_completo, correo_electronico, rol):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                sql = "UPDATE usuarios SET nombre_completo = %s, correo_electronico = %s, rol = %s WHERE id_usuario = %s"
                cursor.execute(sql, (nombre_completo, correo_electronico, rol, id_usuario))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
        finally:
            conexion.close()