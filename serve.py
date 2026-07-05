# serve.py
from waitress import serve
from app import create_app

# Instanciamos la aplicación
app = create_app()

# serve.py - Corregido sin parámetros desconocidos
if __name__ == '__main__':
    print("🚀 Servidor de Producción (Waitress) iniciado...")
    print("Escuchando en http://127.0.0.1:5000")
    
    # Hemos eliminado 'channel_request_limit' para evitar el ValueError
    serve(
        app, 
        host='127.0.0.1', 
        port=5000, 
        threads=100, 
        connection_limit=2000
    )