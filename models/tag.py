from flask_sqlalchemy import SQLAlchemy
from models.post import post_tag, db
#db = SQLAlchemy()

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(10), nullable=False)
