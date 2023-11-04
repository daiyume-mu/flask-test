from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

post_tag= db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))

post_user= db.Table('post_user',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

    comments = db.relationship('Comment', backref='post')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')
    users = db.relationship('User', secondary=post_user, backref='posts')
    

class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance



class PostModel:

    def __init__(self, db_session):
        if not hasattr(self, "db_session"):  
            self.db_session = db_session


    def get_all_posts(self, user_id):
        return (self.db_session.query(Post)
                 .join(post_user, Post.id == post_user.c.post_id)
                 .filter(post_user.c.user_id == user_id)
                 .options(db.joinedload(Post.tags))
                 .order_by(Post.due)
                 .all())
    

    def add_post(self, post):
        self.db_session.add(post)
        self.db_session.commit()


    def associate_user(self, post, user):
        post.users.append(user)
        self.db_session.commit()


    def get_post_by_id(self, id):
        return self.db_session.query(Post).get(id)
                                               

    def update_post(self, post):
        self.db_session.commit()


    def delete_post_by_id(self, id):
        post = self.get_post_by_id(id)
        self.db_session.delete(post)
        self.db_session.commit()