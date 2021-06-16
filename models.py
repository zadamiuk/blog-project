from app import db, bcrypt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class BlogPost(db.Model):
    __tablename__ = "wpis"

    id = db.Column(db.Integer, primary_key=True)
    tytul = db.Column(db.String, nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    tresc = db.Column(db.String, nullable=False)
    autor_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, tytul, data, tresc, autor_id):
        self.tytul = tytul
        self.data = data
        self.tresc = tresc
        self.autor_id = autor_id

    def __repr__(self):
        return '<tytyl{}'.format(self.tytul)


class User(db.Model):
    __tablename__ = "bloger"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    wpis = relationship("BlogPost", backref='autor')

    def __init__(self, login, password):
        self.login = login
        self.password = bcrypt.genetrate_password_hash(password)

    def __repr__(self):
        return '<login{}'.format(self.login)
