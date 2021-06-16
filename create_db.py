from app import db
from models import BlogPost

db.create_all()

db.session.add(BlogPost("Ola", "kolejne", "16/06/2021", "zabawa na całego"))

db.session.commit()