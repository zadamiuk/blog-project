#storzenie pierwszych wartości w bazie danych - tabela wpisów i blogerów
import sqlite3

with sqlite3.connect('baza.db') as connection:
    c = connection.cursor()
    c.execute("CREATE TABLE wpis(autor TEXT, tytul TEXT, data DATE, tresc TEXT)")
    c.execute('INSERT INTO wpis VALUES("Ola", "sprawdza", "29/05/2021", "zabawa na całego")')
    c.execute('INSERT INTO wpis VALUES("Ola1", "sprawdzaxd", "29/05/2021", "zabawa na całego")')
    c.execute("CREATE TABLE bloger(autor TEXT, login TEXT)")
    c.execute('INSERT INTO bloger VALUES ("Ola","ola123")')
    c.execute('INSERT INTO bloger VALUES ("Zuza","zuza123")')
    c.execute('INSERT INTO bloger VALUES ("Asia","asia123")')