from flask_sqlalchemy import SQLAlchemy
from app import db
from hashutils import make_pw_hash

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    pw_hash = db.Column(db.String(120))
    username = db.Column(db.String(50), unique=True)
    post = db.relationship('Post', backref='owner')

    def __init__(self, password, username):
        self.pw_hash = make_pw_hash(password)
        self.username = username
