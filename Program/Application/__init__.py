from flask import Flask
from flask_sqlalchemy import flask_sqlalchemy
from os import getenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.configp['SECRET_KEY'] = getenv("SECRET_KEY")

db = SQLAlchemy(app)

from application import routes