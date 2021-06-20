#storzenie pierwszych wartości w bazie danych - tabela wpisów i blogerów
import sqlite3

with sqlite3.connect('baza.db') as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE bloger(bloger_id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "login TEXT, password TEXT)")
    c.execute('INSERT INTO bloger VALUES (1,"Ola","ola123")')
    c.execute('INSERT INTO bloger VALUES (2,"Zuza","zuza123")')
    c.execute('INSERT INTO bloger VALUES (3,"Asia","asia123")')

    c.execute("CREATE TABLE wpis(wpis_id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "tytul TEXT NOT NULL, data DATE NOT NULL, tresc TEXT NOT NULL)")
              #"login_id INTEGER  NOT NULL REFERENCES bloger)")
    c.execute('INSERT INTO wpis VALUES(1, "Sprawdzenie", "19/06/2021", "zabawa na całego")')
    c.execute('INSERT INTO wpis VALUES(2, "Sprawdzenie vol.2", "19/06/2021", "zabawa na całego hehe")')
    c.execute('INSERT INTO wpis VALUES(3, "Sprawdzenie vol.3", "19/06/2021", "zabawa na całego hehe2")')

