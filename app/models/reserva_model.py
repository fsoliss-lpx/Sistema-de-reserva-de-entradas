# app/models/reserva_model.py
from app import get_db_connection
from datetime import datetime, timedelta

class ReservaModel:
    @staticmethod
    def intentar_reservar(id_asiento, id_usuario, version_actual):
        """
        Aplica el Control Optimista. Si la versión cambió en milisegundos, falla intencionalmente.
        """
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # 1. Intentar actualizar validando la versión exacta
                sql_update = """
                    UPDATE asientos 
                    SET estado = 'RESERVADO_TEMPORAL', version = version + 1 
                    WHERE id_asiento = %s AND version = %s AND estado = 'DISPONIBLE'
                """
                filas_afectadas = cursor.execute(sql_update, (id_asiento, version_actual))
                
                # Si filas_afectadas es 0, alguien más ganó la carrera
                if filas_afectadas == 0:
                    return False

                # 2. Si ganamos el bloqueo, creamos la reserva temporal (TTL 10 minutos)
                expiracion = datetime.now() + timedelta(minutes=10)
                sql_reserva = """
                    INSERT INTO reservas (id_usuario, id_asiento, estado, timestamp_expiracion)
                    VALUES (%s, %s, 'TEMPORAL', %s)
                """
                cursor.execute(sql_reserva, (id_usuario, id_asiento, expiracion))
            
            # Consolidar la transacción ACID
            conexion.commit()
            return cursor.lastrowid # Retorna el ID de la nueva reserva
        except Exception as e:
            conexion.rollback()
            print(f"Error en concurrencia: {e}")
            return False
        finally:
            conexion.close()


    @staticmethod
    def liberar_reservas_expiradas():
        """
        Daemon: Busca reservas temporales cuyo TTL haya vencido y libera los asientos.
        """
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # 1. Buscar las reservas que ya expiraron
                sql_select = """
                    SELECT id_reserva, id_asiento 
                    FROM reservas 
                    WHERE estado = 'TEMPORAL' AND timestamp_expiracion < NOW()
                """
                cursor.execute(sql_select)
                reservas_vencidas = cursor.fetchall()
                
                # 2. Revertir el estado de cada asiento y reserva
                for reserva in reservas_vencidas:
                    # Devolver el asiento a DISPONIBLE
                    cursor.execute("UPDATE asientos SET estado = 'DISPONIBLE' WHERE id_asiento = %s", (reserva['id_asiento'],))
                    # Marcar la reserva como EXPIRADA
                    cursor.execute("UPDATE reservas SET estado = 'EXPIRADA' WHERE id_reserva = %s", (reserva['id_reserva'],))
            
            # 3. Consolidar los cambios
            conexion.commit()
            
            if reservas_vencidas:
                print(f"🧹 Daemon de limpieza: {len(reservas_vencidas)} asiento(s) liberado(s) por inactividad.")
                
        except Exception as e:
            conexion.rollback()
            print(f"Error en el Daemon de limpieza: {e}")
        finally:
            conexion.close()