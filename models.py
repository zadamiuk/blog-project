from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

dataBase = SQLAlchemy()


class User(dataBase.Model):
    __tablename__ = "user"

    id = dataBase.Column(dataBase.Integer, primary_key=True)
    login = dataBase.Column(dataBase.String, nullable=False)
    password = dataBase.Column(dataBase.String, nullable=False)
    #wpis = dataBase.relationship("BlogPost", backref='autor')

    def __init__(self, login, password):
        self.login = login
        self.password = bcrypt.genetrate_password_hash(password)

    def __repr__(self):
        return '<login{}'.format(self.login)


class BlogSfera(dataBase.Model):
    __tablename__ = "wpis"

    id = dataBase.Column(dataBase.Integer, primary_key=True)
    tytul = dataBase.Column(dataBase.String, nullable=False)
    data = dataBase.Column(dataBase.DateTime, nullable=False)
    tresc = dataBase.Column(dataBase.String, nullable=False)
    #autor_id = dataBase.Column(dataBase.Integer, ForeignKey('users.id'))

    def __init__(self, tytul, data, tresc):
        self.tytul = tytul
        self.data = data
        self.tresc = tresc
        #self.autor_id = autor_id

    def __repr__(self):
        return '<tytyl{}'.format(self.tytul)
