from flask_sqlalchemy import SQLAlchemy
from models.post import db
#db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(25), nullable=False)
