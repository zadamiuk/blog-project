import datetime
import sqlite3
from functools import wraps

from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import User, BlogSfera, dataBase

app = Flask(__name__)

app.config['SECRET_KEY'] = 'szalony kod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dataBase.init_app(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


# strona główna z wypisem ogrganiczonych wpisów
@app.route('/')
def welcome():
    conn = dataBaseConn()
    data = conn.execute('SELECT * FROM wpis LIMIT 3').fetchall()
    conn.close()
    return render_template('mainpage.html', data=data)


# strona do rejestracji nowego użytkownika
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login)
        if user:
            flash('You try again!')
            return redirect(url_for('register'))

        newUser = User(login=login, password=password)

        dataBase.session.add(newUser)
        dataBase.session.commit()
        flash('Account has been creates! Log in!')

        return redirect(url_for('login'))

    return render_template('register.html')


# strona do logowania
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login)

        if user and password:
            return redirect(url_for('my'))
        else:
            flash('Try again!')
            return redirect(url_for('login'))

    return render_template('login.html')


# strona użytkownika ze wszystkimi wpisami innych użytkowników
@app.route('/mypage')
def my():
    return render_template('mypage.html')


# wylogowanie użytkownika
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_id', None)
    flash('You are logout. See you soon!')
    return redirect(url_for('welcome'))


# strona do dodania nowej notatki
@app.route('/new', methods=["GET", "POST"])
@login_required
def add():
    if request.method == 'POST':
        tytul = request.form['title']
        tresc = request.form['content']
        data = datetime.date.today()

        if not tytul:
            flash('Tytuł jest obowiązkowy!')
        else:
            newPost = BlogSfera(tytul=tytul, data=data, tresc=tresc)
            dataBase.session.add(newPost)
            dataBase.session.commit()
            flash('Post was created!')
            return redirect(url_for('welcome'))

    return render_template('new.html')


def dataBaseConn():
    conn = sqlite3.connect('baza.db')
    conn.row_factory = sqlite3.Row
    return conn


# uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
