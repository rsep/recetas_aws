from email import message
from flask import render_template, redirect, request, session, flash
from flask_app import app

# importar Modelos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

# PENDIENTE importar Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# En terminal correr: pipenv install flask pymysql flask-bcrypt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    print(request.form['password'])
    # Validar la info que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')
    print(request.form['password']+"2")

    # Guardar Registro
    pwd = bcrypt.generate_password_hash(request.form['password']) #Encriptando la contraseña del usuario y la guardamos en pwd
    print(1)
    # Crear un diccionario con todos los datos del request.form
    formulario={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd #contraseña encriptada
    }
    id = User.save(formulario) #Recibir el identificador del nuevo usuario
    session['user_id'] = id #Guardamos en sesión el identificador del usuario
    print(2)
    return redirect ('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    # Verificar que el email exista en la BD
    user = User.get_by_email(request.form) # Vamos a recibir False o una instancia de usuario

    if not user: #Si user = False
        # flash('E-mail no encontrado', 'login')
        # return redirect('/')
        return jsonify(message="E-mail no encontrado")
    
    # user es una instancia con todos los datos de mi usuario (pero la password está encriptada y no podemos desencriptarla, hay que enviar password encriptado y el que no a bcrypt y ellos validan)
    if not bcrypt.check_password_hash(user.password, request.form['password']): #Verifica que contraseña encriptada haga match con la no encriptada
        # flash('Password incorrecto', 'login')
        # return redirect('/')
        return jsonify(message="Password incorrecto")

    session['user_id'] = user.id
    # return redirect('/dashboard')
    return jsonify(message="correcto")





@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    # Sé que en sesión tengo el id de mi usuario (sesion['user_id'])
    # Quiero una función que en base a ese id me recoge una instancia del usuario
    formulario = {"id": session['user_id']}
    user = User.get_by_id(formulario)

    # Lista con todas las recetas
    recipes = Recipe.get_all()

    return render_template('dashboard.html', user=user, recipes=recipes)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




# MAÑANA Edición & Borrado