# locustfile.py
from locust import HttpUser, task, between
import random
import time

# Cuentas reales registradas en tu BD (asegúrate de que existan)
CUENTAS_EQUIPO = [
    {"correo": "miguel@unemi.edu.ec", "contrasena": "123"},
    {"correo": "allison@unemi.edu.ec", "contrasena": "123"},
    {"correo": "jorge@unemi.edu.ec", "contrasena": "123"}
]

class CompradorConcierto(HttpUser):
    # Tiempo de espera entre tareas (1 a 3 segundos)
    wait_time = between(1, 3)

    def on_start(self):
        """Inicio de sesión una sola vez por usuario virtual."""
        # Espera aleatoria para que no todos lleguen al mismo milisegundo
        time.sleep(random.uniform(0, 3))
        
        self.cuenta_actual = random.choice(CUENTAS_EQUIPO)
        
        # Realizamos el login
        with self.client.post("/auth/login", data={
            "correo": self.cuenta_actual["correo"], 
            "contrasena": self.cuenta_actual["contrasena"]
        }, catch_response=True) as response:
            if "login" in response.url:
                response.failure("Fallo de Login: Las credenciales fueron rechazadas.")
            else:
                response.success()

    @task(1)
    def ver_dashboard(self):
        """Navegación básica."""
        self.client.get("/dashboard/")

    @task(3)
    def intentar_reservar_asiento(self):
        """Tarea principal: Pelea por asientos (ID 1 al 20)."""
        id_asiento = random.randint(1, 20)
        
        # Usamos json para tu API, ajusta según tu controller si es data=
        with self.client.post("/api/reservar/", json={"id_asiento": id_asiento}, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 409:
                # Éxito: el control optimista bloqueó la sobreventa correctamente
                response.success()
            else:
                # Aquí capturamos cualquier otro error inesperado
                response.failure(f"Error {response.status_code}")