from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

post_tag= db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

    comments = db.relationship('Comment', backref='post')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')

"""class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    post = db.relationship('Post', backref='posttag')
    tag = db.relationship('Tag', backref='posttag')"""