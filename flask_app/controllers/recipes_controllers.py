from flask import flash, render_template, redirect, session, request, flash
from flask_app import app

# Importar Modelos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

# Importaciones para subir imágenes
from werkzeug.utils import secure_filename
import os

@app.route('/new/recipe')
def new_recipe():
    # comprobar que un usuario inicio sesion
    if 'user_id' not in session: 
        return redirect('/')
    
    formulario = {'id': session['user_id']}

    # regresa instancia del usuario que inició sesion y la guarda en varuable user 
    user = User.get_by_id(formulario)

    return render_template('new_recipe.html', user=user)


@app.route('/create/recipe',methods=['POST'])
def create_recipe():
    # validar que la perona esta logueado
    if 'user_id' not in session:
        return redirect('/')

    # Validación de receta 
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')
    
    # Validamos que haya subido algo
    if 'image' not in request.files:
        flash('No seleccionó ninguna imagen','receta')
        return redirect('/new/recipe')
    
    image = request.files['image'] #Variable con la imagen

    # Validar que no esté vacío
    if image.filename == '':
        flash('Nombre de imagen vacío','receta')
        return redirect('/new/recipe')
    
    # Agregar nombre a nuestra imagen / Generar de manera segura el nombre de la imagen
    nombre_imagen = secure_filename(image.filename)
    
    # Guardar la imagen
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))

    # Diccionario con todos los datos del formulario
    formulario = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": int(request.form['under_30']),
        "user_id": request.form['user_id'],
        "image": nombre_imagen
    }

    # Guardar la receta
    Recipe.save(formulario)

    return redirect('/dashboard')


@app.route('/edit/recipe/<int:id>')
def editar(id):
    # comprobar que un usuario inicio sesion
    if 'user_id' not in session: 
        return redirect('/')
    
    formulario = {'id': session['user_id']}

    # regresa instancia del usuario que inició sesion y la guarda en varuable user 
    user = User.get_by_id(formulario)

    # obtener la instancia de la receta que se debe desplegar en editar - en base al id que recibimos en url
    formulario_receta = {"id":id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)


@app.route('/update/recipe', methods=['POST'])
def update():
    # verificar que haya iniciado sesion
    if 'user_id' not in session:
        return redirect('/')
    
    # verficar que los datos estan correctos
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['recipe_id'])
        # para obtener la ruta /edit/recipe/1
    
    # Guardar cambios
    Recipe.update(request.form)

    # Redireccionar a /dashboard
    return redirect('/dashboard')


@app.route('/delete/recipe/<int:id>')
def delete(id):
    # verificar que haya iniciado sesion
    if 'user_id' not in session:
        return redirect('/')
    # Revisa que en la variable session exista un user_id

    # borrar receta
    formulario = {"id": id}
    Recipe.delete(formulario)

    # redirigir a dashboard
    return redirect('/dashboard')

@app.route('/view/recipe/<int:id>')
def view(id):
    # verificar inicio de sesion
    if 'user_id' not in session:
        return redirect('/')
    
    # nombre de usuario que inicio sesion
    formulario = {'id': session['user_id']}
    user = User.get_by_id(formulario)
    
    # Mostrar receta porr id
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    # renderizar la template show_recipe
    return render_template('show_recipe.html', user=user, recipe=recipe)