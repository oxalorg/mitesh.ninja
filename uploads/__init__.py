from flask import Flask
from app import app
from uploads import views

# Makes sure the file exists.
with open(app.config['COUNT_FILE'], 'a') as f:
    pass
