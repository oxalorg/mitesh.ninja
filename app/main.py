from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/' + app.config['GOOGLE_VERIFY'])
@app.route('/' + app.config['GOOGLE_VERIFY'] + '.html')
def google_verify():
    return 'google-site-verification: ' + app.config['GOOGLE_VERIFY'] + '.html'
