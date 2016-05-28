from flask import Flask
from app import app
from uploads import views
from uploads import models

# Makes sure the file exists.
with open(app.config['COUNT_FILE'], 'a') as f:
    pass
