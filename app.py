# dodanie odpowiednich bibliotek
import datetime
import sqlite3

from flask import Flask, render_template, request, flash, redirect, url_for, session
from sqlalchemy import desc

from models import User, BlogSfera, dataBase

# stworzenie aplikacji
app = Flask(__name__)

# konfiguracja aplikacji
app.config['SECRET_KEY'] = 'szalony kod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dataBase.init_app(app)


# strona główna z wypisem ogrganiczonych wpisów
@app.route('/')
def welcome():

    data = BlogSfera.query.order_by(desc(BlogSfera.id)).limit(3).all() #wyświetlanie najnowszych wpisów na stronie głównej

    return render_template('mainpage.html', data=data)


# strona do rejestracji nowego użytkownika
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login).first()  # sprawdzenie czy taki login istenieje
        if user:
            flash('You try again!')
            return redirect(url_for('register'))

        newUser = User(login=login, password=password)  # tworzenie nowego użytkownika

        dataBase.session.add(newUser)  # dodanie nowego użytkownika
        dataBase.session.commit()  # potwierdzenie zmian

        flash('Account has been creates! Log in!')

        return redirect(url_for('login'))

    return render_template('register.html')


# strona do logowania
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login).first()  # szukanie loginu w bazie

        if user is not None and password:  # warunek jak znajdziemy login
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('my'))  # login jest to przekierowanie na stronę
        else:
            flash('Try again!')
            return redirect(url_for('login'))  # login błędny powrót na login

    return render_template('login.html')


# strona użytkownika ze wszystkimi wpisami innych użytkowników
@app.route('/mypage')
def my():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = BlogSfera.query.all()

    return render_template('mypage.html', data=data)


# wylogowanie użytkownika
@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        session.pop('user_id', None)
        session['logged_in'] = False
        flash('You are logout. See you soon!')
    return redirect(url_for('welcome'))


# strona do dodania nowej notatki
@app.route('/new', methods=["GET", "POST"])
def add():
    if not session.get('logged_in'):  # jeśli osoba jest zaloogowana może dodać nowy post, jeśli nie to logowanie
        return redirect(url_for('login'))

    if request.method == 'POST':

        tytul = request.form['title']
        tresc = request.form['content']
        data = datetime.date.today()
        user_id = session["user_id"]

        if not tytul:
            flash('Tytuł jest obowiązkowy!')  # warunek na swtorzenie nowego wpisu
        else:
            newPost = BlogSfera(tytul=tytul, data=data, tresc=tresc, user_id=user_id)  # tworzenie nowego wpisu
            dataBase.session.add(newPost)  # dodanie nowego wpisu do bazy
            dataBase.session.commit()  # potwierdzenie zmian
            flash('Post was created!')
            return redirect(url_for('my'))

    return render_template('new.html')


# usuwanie wpisu
@app.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    if not session.get('logged_in'):  # jeśli osoba jest zaloogowana może dodać nowy post, jeśli nie to logowanie
        return redirect(url_for('login'))

    wpis = BlogSfera.query.filter_by(id=id).delete()
    dataBase.session.commit()

    return redirect(url_for('my'))


# funkcja do połączenia z bazą
def dataBaseConn():
    conn = sqlite3.connect('baza.db')
    conn.row_factory = sqlite3.Row
    return conn


# uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
