from flask_sqlalchemy import SQLAlchemy
from models.tag import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

    comments = db.relationship('Comment', backref='post')

