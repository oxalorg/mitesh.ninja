from flask import Flask
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
db = SQLAlchemy(app)

import form
from app import upload

app.register_blueprint(upload.views.upload)
