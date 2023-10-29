import sys
sys.path.append('D:/file/flask-todo-app/develop')
from flask import Flask
from datetime import datetime
from models.post import Post, db
from models.user import User
from models.tag import Tag, TagModel
from models.comment import Comment
from services.post_service import PostService
from services.user_service import UserService
import unittest

postservice = PostService(db.session)
tagservice = TagModel(db.session)
userservice = UserService(db.session)

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
            email = "test@example.com"
            password = "password123"
            user_test = userservice.register_user(email, password)

            tag="SampleTag"
            tag_test = tagservice.create_tag(tag)
            tag_list = [tag_test]
            
            title = "Test"
            detail = "Test Detail"
            due = "2023-10-20"
            post_test = postservice.create_post(title, detail, due)
            postservice.associate_user(post_test, user_test)
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
            email = "test@example.com"
            password = "password123"
            userservice.register_user(email, password)

            title = "test"
            detail = "Test Detail"
            due ="2023-10-20"
            first_count = Post.query.count()
            post = postservice.create_post(title, detail, due)
            new_count = Post.query.count()
            self.assertIsNotNone(post)
            self.assertEqual(new_count, first_count + 1)
            
            db.session.rollback()


    def test_associate_user(self):
        with self.app.app_context():
            email = "test@example.com"
            password = "password123"
            user_test = userservice.register_user(email, password)

            title = "Test"
            detail = "Test Detail"
            due = "2023-10-20"
            post_test = postservice.create_post(title, detail, due)
            
            self.assertEqual(len(post_test.users), 0)
            postservice.associate_user(post_test, user_test)
            self.assertEqual(len(post_test.users), 1)
            self.assertEqual(post_test.users[0].id, user_test.id)


    def test_get_post_by_id(self):
        with self.app.app_context():
            title = "Test"
            detail = "Test Detail"
            due = "2023-10-20"
            postservice.create_post(title, detail, due)

            post = postservice.get_post_by_id(1)
            self.assertIsNotNone(post)
            self.assertEqual(post.title, "Test")
            self.assertEqual(post.detail, "Test Detail")

            db.session.rollback()


    def test_update_post(self):
        with self.app.app_context():
            title = "Test"
            detail = "Test Detail"
            due = "2023-10-20"
            postservice.create_post(title, detail, due)

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
            title = "Test"
            detail = "Test Detail"
            due = "2023-10-20"
            postservice.create_post(title, detail, due)

            first_count = Post.query.count()
            id = 1
            postservice.delete_post(id)
            new_count = Post.query.count()
            self.assertEqual(new_count, first_count - 1)

            db.session.rollback()

if __name__ == '__main__':
    unittest.main()
