from flask_sqlalchemy import SQLAlchemy
from models.post import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.String(500))
    content_timestamp = db.Column(db.DateTime, nullable=False)

    #posts = db.relationship('Post', back_populates='comments')


class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class CommentModel:

    def __init__(self, db_session):
        if not hasattr(self, "db_session"):  
            self.db_session = db_session


    def add_comment(self, comment):
        self.db_session.add(comment)
        self.db_session.commit()