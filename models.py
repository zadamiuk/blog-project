from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy umożliwia nie pisanie trudnych zapytań SQL
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

dataBase = SQLAlchemy()


# model użytkonika
class User(dataBase.Model):
    __tablename__ = "user"

    id = dataBase.Column(dataBase.Integer, primary_key=True)
    login = dataBase.Column(dataBase.String, nullable=False)
    password = dataBase.Column(dataBase.String, nullable=False)

    wpis = relationship("BlogSfera", backref='user')

    def __init__(self, login, password):
        self.login = login
        self.password = bcrypt.genetrate_password_hash(password)

    def __repr__(self):
        return '<login{}'.format(self.login)


# model wpisu
class BlogSfera(dataBase.Model):
    __tablename__ = "wpis"

    id = dataBase.Column(dataBase.Integer, primary_key=True)
    tytul = dataBase.Column(dataBase.String, nullable=False)
    data = dataBase.Column(dataBase.Date, nullable=False)
    tresc = dataBase.Column(dataBase.String, nullable=False)

    user_id = dataBase.Column(dataBase.Integer, ForeignKey('user.id'), nullable=False)  # związek między wpisem a user

    def __init__(self, tytul, data, tresc, user_id):
        self.tytul = tytul
        self.data = data
        self.tresc = tresc
        self.user_id = user_id

    def __repr__(self):
        return '<tytyl{}'.format(self.tytul)
