from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(10), nullable=False)

    posts = db.relationship('Post', backref='tag')