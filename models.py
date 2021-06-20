from flask_login import login_manager
from flask_login._compat import unicode
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

dataBase = SQLAlchemy()

#model użytkonika
class User(dataBase.Model):
    __tablename__ = "user"

    id = dataBase.Column(dataBase.Integer, primary_key=True)
    login = dataBase.Column(dataBase.String, nullable=False)
    password = dataBase.Column(dataBase.String, nullable=False)

    # wpis = dataBase.relationship("BlogPost", backref='autor')

    def __init__(self, login, password):
        self.login = login
        self.password = bcrypt.genetrate_password_hash(password)

    def __repr__(self):
        return '<login{}'.format(self.login)


'''
    def is_authenticated(self):
        return True

    def is_active(self):
         return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
'''

#model wpisu
class BlogSfera(dataBase.Model):
    __tablename__ = "wpis"

    id = dataBase.Column(dataBase.Integer, primary_key=True)
    tytul = dataBase.Column(dataBase.String, nullable=False)
    data = dataBase.Column(dataBase.DateTime, nullable=False)
    tresc = dataBase.Column(dataBase.String, nullable=False)

    # autor_id = dataBase.Column(dataBase.Integer, ForeignKey('users.id')) #związek między wpisem a user

    def __init__(self, tytul, data, tresc):
        self.tytul = tytul
        self.data = data
        self.tresc = tresc
        # self.autor_id = autor_id

    def __repr__(self):
        return '<tytyl{}'.format(self.tytul)
