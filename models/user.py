from flask_sqlalchemy import SQLAlchemy
from models.post import db
#db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(25), nullable=False)

class UserModel:

	def __init__(self, db_session):
		self.db_session = db_session


	def register_user(self, user):
		self.db_session.add(user)
		self.db_session.commit()

	def get_user_by_email(self, email):
		return User.query.filter_by(email=email).first()
	
	def get_user_by_id(self, user_id):
		return User.query.filter_by(id=user_id).first()