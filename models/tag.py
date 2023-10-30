from flask_sqlalchemy import SQLAlchemy
from models.post import Post, post_user, db
from sqlalchemy.orm import joinedload
#db = SQLAlchemy()

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(10), nullable=False)


class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class TagModel:

    def __init__(self, db_session):
        if not hasattr(self, "db_session"):  
            self.db_session = db_session


    def get_posts_by_tag_id(self, tag_id, user_id):
        posts = (self.db_session.query(Post)
                 .join(Post.tags)
                 .join(post_user, Post.id == post_user.c.post_id)
                 .filter(Tag.id == tag_id, post_user.c.user_id == user_id)
                 .options(joinedload(Post.tags))
                 .order_by(Post.due)
                 .all())
        return posts
    

    def add_tag(self, tag):
        self.db_session.add(tag)
        self.db_session.commit()


    def get_all_tags(self):
        return Tag.query.all()


    def associate_tags(self, post, tag_id):
        tags = Tag.query.filter(Tag.id.in_(tag_id)).all()
        post.tags.extend(tags)
        self.db_session.commit()
        print(tags)


    def tag_clear(self, post):
        if post.tags:
            post.tags.clear()