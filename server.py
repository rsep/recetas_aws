# importación de flask_app
from flask_app import app

# importación de controladores
from flask_app.controllers import users_controllers, recipes_controllers

# Ejecucución de la app
if __name__=='__main__':
    app.run(debug=True)