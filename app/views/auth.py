from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario_model import UsuarioModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        if UsuarioModel.registrar_usuario(nombre, correo, contrasena):
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error en el registro. El correo ya podría estar en uso.', 'danger')

    return render_template('auth/registro.html')

# 1. Ruta para ver el formulario (GET)
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('auth/login.html')

# 2. Ruta para procesar el formulario (POST)
@auth_bp.route('/login', methods=['POST'])
def login():
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')

    usuario = UsuarioModel.verificar_login(correo, contrasena)
    
    if usuario:
        session['usuario_id'] = usuario['id_usuario']
        session['rol'] = usuario['rol']
        session['nombre'] = usuario['nombre_completo']
        return redirect(url_for('user.inicio')) # Redirige al dashboard
    else:
        flash('Credenciales incorrectas', 'danger')
        return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login_page'))