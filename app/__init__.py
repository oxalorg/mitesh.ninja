from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

import form
import uploads
