from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario_model import UsuarioModel

auth_bp = Blueprint('auth', __name__)

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

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        usuario = UsuarioModel.verificar_login(correo, contrasena)
        
        if usuario:
            # Guardamos datos en la sesión[cite: 5]
            session['usuario_id'] = usuario['id_usuario']
            session['rol'] = usuario['rol']
            session['nombre'] = usuario['nombre_completo']
            
            # Redirección según el rol (Para el Sprint 2 y 8)
            if usuario['rol'] == 'ADMINISTRADOR':
                return redirect('/admin') # Ruta futura del admin
            else:
                return redirect('/dashboard') # Ruta futura del usuario
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))