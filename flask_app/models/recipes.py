from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.image = data['image']

        # LEFT JOIN
        self.first_name = data['first_name']

    # validar recipe
    @staticmethod
    def valida_receta(formulario):
        is_valid = True

        if len(formulario['name']) < 3:
            flash("El nombre de la receta debe tener al menos 3 caracteres",'receta')
            is_valid = False
        
        if len(formulario['description']) < 3:
            flash("La descripción de la receta debe tener al menos 3 caracteres",'receta')
            is_valid = False
        
        if len(formulario['instructions']) < 3:
            flash("Las instrucciones de la receta deben tener al menos 3 caracteres",'receta')
            is_valid = False
        
        if formulario['date_made'] == '':
            flash("Ingrese una fecha",'receta')
            is_valid = False

        return is_valid
    

    # función guardar recipe
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO recipes(name,description,instructions,date_made,under_30,user_id,image) VALUES(%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s,%(user_id)s,%(image)s)"
        result = connectToMySQL('esquema_recetas').query_db(query,formulario)
        return result


    # show all recipes by id_user
    @classmethod
    def get_all(cls):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('esquema_recetas').query_db(query) # Lista de diccionarios
        recipes = []

        for recipe in results:
            recipes.append(cls(recipe))
        
        return recipes


    # edit recipe by id
    @classmethod
    def get_by_id(cls,formulario):
        query = "SELECT recipes.*, first_name FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        result = connectToMySQL('esquema_recetas').query_db(query,formulario) # Lista de solo un diccionario adentro
        recipe = cls(result[0]) #result[0] = diccionario con todos los datos de la receta
        # cuando hacemos el cls de result creamos la instancia en base a ese diccionario    
        return recipe

    @classmethod
    def update(cls, formulario):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s,date_made=%(date_made)s, under_30=%(under_30)s WHERE id = %(recipe_id)s"
        # es recipe_id porque ese es el 'name' que tiene el input hidden
        result = connectToMySQL('esquema_recetas').query_db(query,formulario)
        return result
    
    # Función eliminar recet
    @classmethod
    def delete(cls,formulario):
        # Este formulario será un diccionario que contenga la id con la receta a borrar nomas
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query,formulario)
        return result

