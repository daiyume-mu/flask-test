import sys
sys.path.append('D:/file/flask-todo-app/develop')
from flask import Flask
import unittest
from models.post import Post, db
from models.user import User
from models.tag import Tag, TagModel
from models.post import Post,db
from models.comment import Comment
from datetime import datetime

tagservice = TagModel(db.session)

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
            tag_test = Tag(tag_name="SampleTag")
            db.session.add(tag_test)
            
            tag = tagservice.get_all_tags()
            self.assertIsInstance(tag, list)
            self.assertEqual(tag[0].tag_name, "SampleTag")

            db.session.rollback()

    def test_associate_tags(self):
        with self.app.app_context():
            converted_due = datetime.strptime("2023-10-20", '%Y-%m-%d')
            post_test = Post(title="Test", detail="Test Detail", due=converted_due)
            db.session.add(post_test)
            db.session.commit()

            post = Post.query.get(1)
            tag = Tag(tag_name="SampleTag")
            db.session.add(tag)
            db.session.commit()
            self.assertNotIn(tag, post.tags)
            tagservice.associate_tags(post, [tag.id])
            new_post = Post.query.get(1)
            self.assertIn(tag, new_post.tags)

            db.session.rollback()

    def test_tag_clear(self):
        with self.app.app_context():
            tag_test = Tag(tag_name="SampleTag")
            db.session.add(tag_test)
            tag_list = [tag_test]
            
            converted_due = datetime.strptime("2023-10-20", '%Y-%m-%d')
            post_test = Post(title="Test", detail="Test Detail", due=converted_due)
            db.session.add(post_test)
            post_test.tags.extend(tag_list)
            db.session.commit()

            post = Post.query.get(1)
            tagservice.tag_clear(post)
            self.assertFalse(post.tags)

            db.session.rollback()

if __name__ == '__main__':
    unittest.main()