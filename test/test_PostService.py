import sys
sys.path.append('D:/file/flask-todo-app/develop')
from flask import Flask
from datetime import datetime
from models.post import Post, db
from models.user import User
from models.tag import Tag
from models.comment import Comment
from services.post_service import PostService
import unittest

postservice = PostService(db.session)

class Test_PostService(unittest.TestCase):

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

    def test_get_all_posts(self):
        with self.app.app_context():
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

            post = postservice.get_all_posts(1)
            print(post)
            self.assertIsNotNone(post)
            self.assertIsInstance(post, list)
            self.assertEqual(post[0].title, "Test")
            self.assertEqual(post[0].tags[0].tag_name, "SampleTag")

            db.session.rollback()

    def test_create_post(self):
        with self.app.app_context():
            user_test = User(email="test@example.com", password="password123")
            db.session.add(user_test)
            db.session.commit()

            title = "test"
            detail = "Test Detail"
            due ="2023-10-20"
            user = User.query.get(1)
            first_count = Post.query.count()
            post = postservice.create_post(title, detail, due, user)
            new_count = Post.query.count()
            self.assertIsNotNone(post)
            self.assertEqual(new_count, first_count + 1)
            
            db.session.rollback()

    def test_get_post_by_id(self):
        with self.app.app_context():
            converted_due = datetime.strptime("2023-10-20", '%Y-%m-%d')
            post_test = Post(title="Test", detail="Test Detail", due=converted_due)
            db.session.add(post_test)
            db.session.commit()

            post = postservice.get_post_by_id(1)
            self.assertIsNotNone(post)
            self.assertEqual(post.title, "Test")
            self.assertEqual(post.detail, "Test Detail")

            db.session.rollback()

    def test_update_post(self):
        with self.app.app_context():
            converted_due = datetime.strptime("2023-10-20", '%Y-%m-%d')
            post_test = Post(title="Test", detail="Test Detail", due=converted_due)
            db.session.add(post_test)
            db.session.commit()
            post = Post.query.get(1)
            self.assertEqual(post.title, "Test")
            self.assertEqual(post.detail, "Test Detail")

            id = 1
            title = "Test re"
            detail = "Test Detail re"
            due = "2023-10-21"
            postservice.update_post(id, title, detail, due)
            post = Post.query.get(1)
            self.assertEqual(post.title, "Test re")
            self.assertEqual(post.detail, "Test Detail re")

            db.session.rollback()

    def test_delete_post(self):
        with self.app.app_context():
            converted_due = datetime.strptime("2023-10-20", '%Y-%m-%d')
            post_test = Post(title="Test", detail="Test Detail", due=converted_due)
            db.session.add(post_test)
            db.session.commit()

            first_count = Post.query.count()
            id = 1
            postservice.delete_post(1)
            new_count = Post.query.count()
            self.assertEqual(new_count, first_count - 1)

            db.session.rollback()

if __name__ == '__main__':
    unittest.main()
