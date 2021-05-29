#https://www.youtube.com/playlist?list=PLLjmbh6XPGK4ISY747FUHXEl9lBxre4mM
#na podstawie tego coś tam sobie pisałam

# zaimportowanie framework Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3

#stworzenie obiektu aplikacji
app = Flask(__name__)
#aplikacja z bazą
app.database = "baza.db"

#potrzebne do session - każde logowanie to inna sesja - trzeba to przemyśleć
app.secret_key = "sprawdzenie"


@app.route('/')
def home():
    return "Hello, world"

#potem zmienić na '/' sprawdzam czy wszystko pyka
@app.route('/welcome')
def welcome():
    g.db = connect_db() #łączenie z bazą
    cur = g.db.execute('SELECT * FROM wpis LIMIT 3') #wyszukanie 3 postów
    wpis = [dict(tytul = row[0], tresc = row[1], autor = row[2]) for row in cur.fetchall()] # wyświetlenie trzech postów
    g.db.close() #zamknięcie połączenia z bazą
    return render_template('strona-glowna.html', posts = wpis)

@app.route('/logowanie', methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Błąd!. Podaj jeszcze raz!'
        else:
            session['logged_id'] = True
            flash('Zostałeś zalogowany')
            return redirect(url_for('home'))
    return render_template("logowanie.html", error = error)

@app.route('/wylogowanie')
def logout():
    session.pop('logged_id', None)
    flash('Zostałeś wylogowany. Do następnego razu!')
    return redirect(url_for('home'))


#metoda do połączenia z bazą danych
def connect_db():
    return sqlite3.connect(app.database)


# start aplikacji wywołane metodą 'run()'
if __name__ == '__main__':
    app.run(debug=True)