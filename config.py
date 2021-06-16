#konfiguracja aplikacji
class BaseConfig(object):
    DEBUG = False
    #pomyslec na jakims fancy kluczem
    SECRET_KEY = 'sprawdzenie'
    SQLALCHEMY_DATABASE_URI = 'sqlite://baza.db'

