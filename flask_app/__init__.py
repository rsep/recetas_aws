# importar flask
from flask import Flask

# inicializar app
app = Flask(__name__)

# secret key for session
app.secret_key = "clave secretisima"

app.config['UPLOAD_FOLDER'] = 'flask_app/static/img'