from app import db
import datetime


class FileDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    filename = db.Column(db.String(120))
    size = db.Column(db.Integer)
    creation_time = db.Column(db.DateTime)
    views = db.Column(db.Integer)
    path = db.Column(db.String(120))

    def __init__(self, filename, name, size, path):
        self.filename = filename
        self.name = name
        self.size = size
        self.path = path
        self.creation_time = datetime.datetime.now()
        self.views = 0

    def __repr__(self):
        return 'Details:\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(
            self.filename, self.name, self.size, self.path, self.creation_time,
            self.views)
