from app import db

class BlogPost(db.Model):
    __tablename__ = "wpis"

    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String, nullable=False)
    tytul = db.Column(db.String, nullable=False)
    data = db.Column(db.Date, nullable=False)
    tresc = db.Column(db.String, nullable=False)

    def __init__(self, autor, tytul, data, tresc):
        self.autor = autor
        self.tytul = tytul
        self.data = data
        self.tresc = tresc

    def __repr__(self):
        return  '<tytyl{}'.format(self.tytul)