import sys
sys.path.append('D:/file/flask-todo-app/develop')
from flask import Flask
import unittest
from models.post import Post, db
from models.user import User
from models.tag import Tag, TagModel
from models.post import Post,db
from models.comment import Comment
from services.post_service import PostService
from services.user_service import UserService
from datetime import datetime

postservice = PostService(db.session)
tagservice = TagModel(db.session)
userservice = UserService(db.session)

class Test_TagService(unittest.TestCase):

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
    
    def test_get_post_by_id(self):
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

            tag_id = 1 
            user_id = 1
            posts = tagservice.get_posts_by_tag_id(tag_id, user_id)
            self.assertIsNotNone(posts)
            self.assertIsInstance(posts, list)
            self.assertEqual(posts[0].title, "Test")

            db.session.rollback()


    def test_create_tag(self):
        with self.app.app_context():
            tag_test = Tag(tag_name="SampleTag")
            db.session.add(tag_test)

            first_count = Tag.query.count()
            tag = "SampleTag2"
            tagservice.create_tag(tag)
            new_count = Tag.query.count()
            self.assertEqual(new_count, first_count + 1)

            db.session.rollback()


    def test_get_all_tags(self):
        with self.app.app_context():
            tag="SampleTag"
            tagservice.create_tag(tag)
            
            tag = tagservice.get_all_tags()
            self.assertIsInstance(tag, list)
            self.assertEqual(tag[0].tag_name, "SampleTag")

            db.session.rollback()


    def test_associate_tags(self):
        with self.app.app_context():
            title = "Test"
            detail = "Test Detail"
            due = "2023-10-20"
            postservice.create_post(title, detail, due)

            post = Post.query.get(1)
            tag="SampleTag"
            tag_test = tagservice.create_tag(tag)
            db.session.commit()
            self.assertNotIn(tag_test, post.tags)
            tagservice.associate_tags(post, [tag_test.id])
            new_post = Post.query.get(1)
            self.assertIn(tag_test, new_post.tags)

            db.session.rollback()


    def test_tag_clear(self):
        with self.app.app_context():
            tag="SampleTag"
            tag_test = tagservice.create_tag(tag)
            tag_list = [tag_test]
            
            title = "Test"
            detail = "Test Detail"
            due = "2023-10-20"
            post_test = postservice.create_post(title, detail, due)
            post_test.tags.extend(tag_list)
            db.session.commit()

            post = Post.query.get(1)
            tagservice.tag_clear(post)
            self.assertFalse(post.tags)

            db.session.rollback()

if __name__ == '__main__':
    unittest.main()