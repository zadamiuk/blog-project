import datetime
import sqlite3

from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import User, BlogSfera, dataBase
from flask_login import login_required, login_user, logout_user, LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'szalony kod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dataBase.init_app(app)
# login_manager = LoginManager()
# login_manager.init_app(app)

# login_manager.login_view = "users.login"
'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

'''


# strona główna z wypisem ogrganiczonych wpisów
@app.route('/')
def welcome():
    conn = dataBaseConn()
    data = conn.execute('SELECT * FROM wpis LIMIT 3').fetchall()  # wypisanie 3 wpisów
    # trzeba zmienić na najnowsze, że by się wyświetlały
    conn.close()
    return render_template('mainpage.html', data=data)


# strona do rejestracji nowego użytkownika
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login)  # sprawdzenie czy taki login istenieje
        if user:
            flash('You try again!')
            return redirect(url_for('register'))

        newUser = User(login=login, password=password)  # tworzenie nowego użytkownika

        dataBase.session.add(newUser)  # dodanie nowego użytkownika
        dataBase.session.commit()  # potwierdzenie zmian
        # login_user(user)
        flash('Account has been creates! Log in!')

        return redirect(url_for('login'))

    return render_template('register.html')


# strona do logowania
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':

        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login)  # szukanie loginu w bazie

        if user is not None and password:  # warunek jak znajdziemy login
            # login_user(user)
            return redirect(url_for('my'))  # login jest to przekierowanie na stronę
        else:
            flash('Try again!')
            return redirect(url_for('login'))  # login błędny powrót na login

    return render_template('login.html')


# strona użytkownika ze wszystkimi wpisami innych użytkowników
@app.route('/mypage')
def my():
    conn = dataBaseConn()
    data = conn.execute('SELECT * FROM wpis').fetchall()  # wypisanie wszystkich postów
    conn.close()
    return render_template('mypage.html', data=data)


# wylogowanie użytkownika
@app.route('/logout')
def logout():
    # logout_user()
    session.pop('logged_id', None)
    flash('You are logout. See you soon!')
    return redirect(url_for('welcome'))


# strona do dodania nowej notatki
@app.route('/new', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        tytul = request.form['title']
        tresc = request.form['content']
        data = datetime.date.today()

        if not tytul:
            flash('Tytuł jest obowiązkowy!')  # warunek na swtorzenie nowego wpisu
        else:
            newPost = BlogSfera(tytul=tytul, data=data, tresc=tresc)  # tworzenie nowego wpisu
            dataBase.session.add(newPost)  # dodanie nowego wpisu do bazy
            dataBase.session.commit()  # potwierdzenie zmian
            flash('Post was created!')
            return redirect(url_for('welcome'))

    return render_template('new.html')


# funkcja do połączenia z bazą
def dataBaseConn():
    conn = sqlite3.connect('baza.db')
    conn.row_factory = sqlite3.Row
    return conn


# uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
