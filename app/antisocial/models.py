from app import db
import datetime


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    files = db.relationship('PostFiles', backref='post')
    creation_time = db.Column(db.DateTime)

    def __init__(self, body):
        self.body = body
        self.creation_time = datetime.datetime.now()


class PostFiles(db.Model):
    __tablename__ = 'post_files'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    url = db.Column(db.String(120))

    def __init__(self, post_id, url):
        self.post_id = post_id
        self.url = url
