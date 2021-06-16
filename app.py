# https://www.youtube.com/playlist?list=PLLjmbh6XPGK4ISY747FUHXEl9lBxre4mM
# na podstawie tego coś tam sobie pisałam


import sqlite3
import SQLAlchemy as SQLAlchemy

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

from models import User

# stworzenie obiektu aplikacji
app = Flask(__name__)

app.config['SECRET_KEY'] = 'szalony kod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'


db = SQLAlchemy(app)
db.create_all()
db.session.commit()


# autoryzacja/ uwierzytelnienie
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))

    return wrap


# strona główna
@app.route('/')
def welcome():
    conn = sqlite3.connect("baza.db")
    cursor = conn.cursor()

    query = "SELECT * FROM wpis LIMIT 3"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()

    return render_template('mainpage.html', data=data)


# możliwość dodania nowego wpisu
@app.route('/add', methods=["GET"])
def add():
    try:
        conn = sqlite3.connect("baza.db")
        cursor = conn.cursor()

        query = "SELECT * FROM wpis"
        cursor.execute(query, )
        data = cursor.fetchall()
        conn.commit()

        return render_template('new.html', data=data)
    except Exception as err:
        return "Error!" + str(err), 500


@app.route('/add', methods=["POST"])
def add_db():
    try:
        #mautor = request.form["autor"]
        mtytul = request.form["tytul"]
        mdata = request.form["data"]
        mtresc = request.form["tresc"]

        conn = sqlite3.connect("baza.db")
        cursor = conn.cursor()

        query = "INSERT INTO wpis(tytul, data, tresc) VALUES(?,?,?,?)"
        cursor.execute(query, (mtytul, mdata, mtresc))
        conn.commit()
        conn.close()

        return redirect(url_for(welcome))
    except Exception as err:
        return "Error!" + str(err), 500


# możliwość edycji wybranego postu
@app.route('/edit/<int:id>', methods=["GET"])
def edit(id):
    try:
        conn = sqlite3.connect("baza.db")
        cursor = conn.cursor()

        query = "SELECT * FROM wpis WHERE id =?"
        cursor.execute(query, (id,))
        data = cursor.fetchall()
        conn.commit()
        conn.close()

        return render_template('modify.html', data=data[0])
    except Exception as err:
        return "Error!" + str(err), 500


@app.route('/edit', methods=["POST"])
def edit_db():
    try:
        mtresc = request.form['tresc']

        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()

        query = "UPDATE wpis SET tresc=?"
        cursor.execute(query, mtresc)
        conn.commit()
        conn.close()

        return redirect(url_for(welcome))
    except Exception as err:
        return "Error!" + str(err), 500


# możliwość usunięcia - bez metody POST, żeby od razu z ikonki można było usunąć
@app.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    try:
        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()

        query = "DELETE FROM wpis WHERE id=?"
        cursor.execute(query, (id,))
        conn.commit()
        conn.close()

        return redirect(url_for('welcome'))
    except Exception as err:
        return "Error!" + str(err), 500


# strona do logowania
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        # na razie zrobione wg tutorialu trzeb będzię połączyć się z baza aby wyszukiwało
        # użytkowników
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Error! Please try again!'
        else:
            session['logged_id'] = True
            flash('You are login!')
            return redirect(url_for('welcome'))
    return render_template("login.html", error=error)


# wylogowanie
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_id', None)
    flash('You are logout. See you soon!')
    return redirect(url_for('welcome'))




# start aplikacji wywołane metodą 'run()'
if __name__ == '__main__':
    app.run(debug=True)
