# https://www.youtube.com/playlist?list=PLLjmbh6XPGK4ISY747FUHXEl9lBxre4mM
# na podstawie tego coś tam sobie pisałam

# zaimportowanie framework Flask
from flask import Flask, render_template, request, redirect, url_for, session, flash, g

import sqlite3

# stworzenie obiektu aplikacji
app = Flask(__name__)

# potrzebne do session - każde logowanie to inna sesja - trzeba to przemyśleć
app.secret_key = "sprawdzenie"

#strona główna
@app.route('/')
def welcome():
    conn = sqlite3.connect("baza.db")
    cursor = conn.cursor()

    query = "SELECT * FROM wpis LIMIT 3"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    conn.close()

    return render_template('strona.html', data=data)

#możliwość dodania nowego wpisu
@app.route('/add', methods=["GET"])
def add():
    try:
        conn = sqlite3.connect("baza.db")
        cursor = conn.cursor()

        query = "SELECT * FROM wpis"
        cursor.execute(query,)
        data = cursor.fetchall()
        conn.commit()

        return render_template('nowy-post.html', data=data)
    except Exception as err:
        return "Error!" + str(err), 500

@app.route('/add', methods=["POST"])
def add_db():
    try:
        mautor = request.form["autor"]
        mtytul = request.form["tytul"]
        mdata = request.form["data"]
        mtresc = request.form["tresc"]

        conn = sqlite3.connect("baza.db")
        cursor = conn.cursor()

        query = "INSERT INTO wpis(autor, tytul, data, tresc) VALUES(?,?,?,?)"
        cursor.execute(query, (mautor, mtytul, mdata, mtresc))
        conn.commit()
        conn.close()

        return  redirect(url_for(welcome))
    except Exception as err:
        return "Error!" + str(err), 500

#możliwość edycji wybranego postu
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

        return render_template('modyfikacja.html', data=data[0])
    except Exception as err:
        return "Error!" + str(err), 500

@app.route('/edit', methods = ["POST"])
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

#możliwość usunięcia - bez metody POST, żeby od razu z ikonki można było usunąć
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

@app.route('/logowanie', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Błąd!. Podaj jeszcze raz!'
        else:
            session['logged_id'] = True
            flash('Zostałeś zalogowany')
            return redirect(url_for('home'))
    return render_template("logowanie.html", error=error)


@app.route('/wylogowanie')
def logout():
    session.pop('logged_id', None)
    flash('Zostałeś wylogowany. Do następnego razu!')
    return redirect(url_for('welcome'))

# start aplikacji wywołane metodą 'run()'
if __name__ == '__main__':
    app.run(debug=True)
