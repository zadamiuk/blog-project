#storzenie pierwszych wartości w bazie danych - tabela wpisów i blogerów
import sqlite3

with sqlite3.connect('baza.db') as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "login TEXT, password TEXT)")
    c.execute('INSERT INTO user VALUES (1,"Ola","ola123")')
    c.execute('INSERT INTO user VALUES (2,"Zuza","zuza123")')
    c.execute('INSERT INTO user VALUES (3,"Asia","asia123")')
    #wszystkie hasla powinny byc hashowane, wiec nasze tez, ale to na potem

    c.execute("CREATE TABLE wpis(id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "tytul TEXT NOT NULL, data DATE NOT NULL, tresc TEXT NOT NULL,"
              "user_id INTEGER NOT NULL REFERENCES user)")
    c.execute('INSERT INTO wpis VALUES(1, "Sprawdzenie", "2019-06-20", "zabawa na całego",1)')
    c.execute('INSERT INTO wpis VALUES(2, "Sprawdzenie vol.2", "2019-06-20", "zabawa na całego hehe",2)')
    c.execute('INSERT INTO wpis VALUES(3, "Sprawdzenie vol.3", "2019-06-20", "zabawa na całego hehe2",3)')

