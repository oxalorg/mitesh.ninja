from app import db, app, basic_auth
from flask import redirect, Response
from flask_admin import Admin
from flask_admin.contrib import sqla
from app.antisocial.models import Post, PostFiles
from app.upload.models import FileDetails
from werkzeug.exceptions import HTTPException

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

admin = Admin(app, name='ninjas-nest')
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(PostFiles, db.session))
admin.add_view(ModelView(FileDetails, db.session))
