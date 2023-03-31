from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos Modelo
from flask_app.models.users import User

#Importación de BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #validamos la informacion que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')
    
    #encriptar contraseña
    pwd = bcrypt.generate_password_hash(request.form['password'])
    
    #creamos un diccionario con todos los datos del request.form
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd}
    
    id = User.save(formulario) #recibimos el id del nuevo usuario registrado
    
    session['user_id'] = id
    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #verificar que existe el correo en la base de datos
    user = User.get_by_email(request.form) #opciones 1. nos regresa false 2. nos regresa en usuario
    
    if not user: #variable user = false
        flash("Email no encontrado", "inicio_sesion")
        return redirect('/')
    
    # user = una instancia con todos los datos del usuario
    #bcrypt.check_password_hash(PASSWORD ENCRIPTADO, PASSWORD SIN ENCRIPTAR) ->True si concide, False si no
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Contraseña incorrecta", "inicio_sesion")
        return redirect('/')
    
    session['user_id'] = user.id #guardamos en session el id del usuario
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    #verifico que exisra user_id en sesion
    if 'user_id' not in session:
        return redirect('/')
    
    #yo se que en sesion tengo guardado el id del usuario que inicio sesion -> session['user_id']
    #queremos que en base a la funcion get_by_id,mandemos un diccionario con el id y no regrese el usuario
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)
    
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')