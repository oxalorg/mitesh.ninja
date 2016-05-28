from flask import Flask
from app import app
from app.upload import views
from app.upload import models

# Makes sure the file exists.
with open(app.config['COUNT_FILE'], 'a') as f:
    pass
