#storzenie pierwszych wartości w bazie danych - tabela wpisów i blogerów
import sqlite3

with sqlite3.connect('baza.db') as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "login TEXT, password TEXT)")
    c.execute('INSERT INTO user VALUES (1,"Ola","ola123")')
    c.execute('INSERT INTO user VALUES (2,"Zuza","zuza123")')
    c.execute('INSERT INTO user VALUES (3,"Asia","asia123")')


    c.execute("CREATE TABLE wpis(id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "tytul TEXT NOT NULL, data DATE NOT NULL, tresc TEXT NOT NULL,"
              "user_id INTEGER NOT NULL REFERENCES user, autor TEXT NOT NULL)")
    c.execute('INSERT INTO wpis VALUES(1, "Wspomnienie z wakacji", "2019-07-25", "Hiszpania jest piękna",1,"Ola")')
    c.execute('INSERT INTO wpis VALUES(2, "Koncert w Warszawie", "2019-05-18", "Na koncercie wystąpił Mata",2,"Zuza")')
    c.execute('INSERT INTO wpis VALUES(3, "3 koktajle na lato", "2021-06-20", "Potrzebujemy 4 składników",3,"Asia")')

