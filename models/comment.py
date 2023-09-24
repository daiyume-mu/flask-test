from flask_sqlalchemy import SQLAlchemy
from models.post import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.String(500))
    content_timestamp = db.Column(db.DateTime, nullable=False)

    #posts = db.relationship('Post', back_populates='comments')