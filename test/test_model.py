import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.post import Post, db
from models.tag import Tag
from models.user import User
from models.comment import Comment
from datetime import datetime

class TestModel(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        
        with self.app.app_context():
            db.create_all()

            user_test = User(email="test@example.com", password="password123")
            db.session.add(user_test)
        
            tag_test = Tag(tag_name="SampleTag")
            db.session.add(tag_test)
            tag_list = [tag_test]
            
            converted_due = datetime.strptime("2023-10-20", '%Y-%m-%d')
            post_test = Post(title="Test", detail="Test Detail", due=converted_due)
            db.session.add(post_test)
            post_test.users.append(user_test)
            post_test.tags.extend(tag_list)
            db.session.commit()

            comment_time = datetime.now() 
            comment_test = Comment(post_id=1, content="Test comment", content_timestamp=comment_time)
            db.session.add(comment_test)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()