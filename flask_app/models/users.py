from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
# patrón email regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # Expresion regular de email


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password =data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    

    # validar inputs
    @staticmethod
    def valida_usuario(formulario):
        # formulario = DICCIONARIO con todos los names y valores que el usaurio ingresa
        # ir validando 1 a 1 todos los campos correspondiente, el formulario es valido hasta que comprobemos que no es valido
        es_valido = True

        # Validamos que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash('Nombre debe tener al menos 3 caracteres', 'registro') #el segundo parametro, es en teoria como una categoria al flash, cuando imprimamos el mensaje queremos que se despliegue lo que tengamos en categoria o etiquta 'registro'
            es_valido = False
        
        # Validar que el apellido tenga al menos 3 caracteres
        if len(formulario['last_name']) < 3:
            flash('Apellido debe tener al menos 3 caracteres', 'registro')
            es_valido = False

        # Verificar que password tenga al menos 6 caracteres
        if len(formulario['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False
        
        # Verificar que las passwords coincidan
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas no coinciden','registro')
            es_valido = False

        # Verificar que el mail tenga el formato correcto con regex
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail inválido','registro')
            es_valido = False
        
        # Consultar si existe el correo electronico (conectar a BD y hacer un query)
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_recetas').query_db(query,formulario)
        if len(results) >= 1:
            flash('E-mail registrado previamente','registro')
            es_valido = False
        
        return es_valido

    # save user
    @classmethod
    def save(cls, formulario):
        query = 'INSERT INTO users(first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)'
        result = connectToMySQL('esquema_recetas').query_db(query,formulario)
        return result
    
    # get user by email
    @classmethod
    def get_by_email(cls,formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('esquema_recetas').query_db(query, formulario) # SELECT me regresa una lista con dicc
        
        if len(result) < 1: # Significa que mi lista está vacía, entonces NO existe ese email
            return False
        else:
            # Me regresa una lista con UN registro, correspondiente al usuario de ese mail
            user = cls(result[0]) # Instanciar el objeto
            return user

    # get user by id
    @classmethod
    def get_by_id(cls,formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas').query_db(query,formulario)
        user = cls(result[0]) #Creando una instancia de user
        return user