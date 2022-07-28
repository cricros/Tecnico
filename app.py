from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateRuntimeError
from routes.unitModel import uModel
from config import DATABASE_CONNECTION_URI

app = Flask(__name__)

#configurando bd
app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLAlchemy(app)
Marshmallow(app)

#rutas de las apis 
app.register_blueprint(uModel)

