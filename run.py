from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.reserva_model import ReservaModel

app = create_app()

def iniciar_limpieza():
    # Esta función llama a nuestro modelo de base de datos
    ReservaModel.liberar_reservas_expiradas()

if __name__ == '__main__':
    # 1. Configurar el planificador
    scheduler = BackgroundScheduler()
    
    # 2. Programar la tarea para que se ejecute cada 60 segundos
    scheduler.add_job(func=iniciar_limpieza, trigger="interval", seconds=60)
    scheduler.start()
    
    try:
        # Importante: use_reloader=False evita que el Daemon se duplique en modo debug
        app.run(debug=True, port=5000, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        # Apagar el Daemon limpiamente si cerramos la consola
        scheduler.shutdown()