import sys
sys.path.append('D:/file/flask-todo-app/develop')
from flask import Flask
from datetime import datetime
from models.post import Post, db
from models.comment import Comment
from models.tag import Tag
from models.user import User
from services.comment_service import CommentService
import unittest


commentservice = CommentService(db.session)

class Test_CommentService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_comment_post(self):
        with self.app.app_context():
            converted_due = datetime.strptime("2023-10-20", '%Y-%m-%d')
            post_test = Post(title="Test", detail="Test Detail", due=converted_due)
            db.session.add(post_test)
            db.session.commit()
            
            post_id = 1 
            content = "test comment"
            comment_time = datetime.now()
            first_count = Comment.query.filter_by(post_id=post_id).count()
            commentservice.comment_post(post_id, content, comment_time)
            new_count = Comment.query.filter_by(post_id=post_id).count()
            self.assertEqual(new_count, first_count + 1)

            db.session.rollback()

if __name__ == '__main__':
    unittest.main()
