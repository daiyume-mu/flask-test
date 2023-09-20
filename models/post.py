from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

    comments = db.relationship('CommentDate', back_populates='post')

class CommentDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comment = db.Column(db.String(500))
    comment_timestamp = db.Column(db.DateTime, nullable=False)

    post = db.relationship('Post', back_populates='comments')