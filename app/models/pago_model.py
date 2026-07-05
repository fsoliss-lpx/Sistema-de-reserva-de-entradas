# app/models/pago_model.py
from app import get_db_connection
from datetime import datetime

class PagoModel:
    @staticmethod
    def procesar_pago(id_reserva, id_usuario, simulacion_exitosa, monto):
        conexion = get_db_connection()
        try:
            with conexion.cursor() as cursor:
                # 1. Validar que la reserva pertenezca al usuario y siga TEMPORAL
                cursor.execute("SELECT id_asiento, estado FROM reservas WHERE id_reserva = %s AND id_usuario = %s", (id_reserva, id_usuario))
                reserva = cursor.fetchone()

                if not reserva or reserva['estado'] != 'TEMPORAL':
                    return False, "La reserva no es válida o su tiempo expiró."

                id_asiento = reserva['id_asiento']
                fecha_actual = datetime.now()

                if simulacion_exitosa:
                    # Escenario de Éxito
                    cursor.execute("UPDATE reservas SET estado = 'CONFIRMADA' WHERE id_reserva = %s", (id_reserva,))
                    cursor.execute("UPDATE asientos SET estado = 'VENDIDO' WHERE id_asiento = %s", (id_asiento,))
                    cursor.execute("INSERT INTO pagos (id_reserva, monto, estado, fecha_pago) VALUES (%s, %s, 'EXITOSO', %s)", (id_reserva, monto, fecha_actual))
                    mensaje = "¡Pago exitoso! Tu entrada ha sido confirmada."
                else:
                    # Escenario de Fallo
                    cursor.execute("UPDATE reservas SET estado = 'CANCELADA' WHERE id_reserva = %s", (id_reserva,))
                    cursor.execute("UPDATE asientos SET estado = 'DISPONIBLE' WHERE id_asiento = %s", (id_asiento,))
                    cursor.execute("INSERT INTO pagos (id_reserva, monto, estado, fecha_pago) VALUES (%s, %s, 'FALLIDO', %s)", (id_reserva, monto, fecha_actual))
                    mensaje = "El pago fue rechazado. El asiento ha sido liberado."

            # 2. Consolidar la transacción
            conexion.commit()
            return True, mensaje
        except Exception as e:
            conexion.rollback()
            print(f"Error en transacción de pago: {e}")
            return False, "Error interno del servidor al procesar el pago."
        finally:
            conexion.close()