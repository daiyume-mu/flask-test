import sys
sys.path.append('D:/file/flask-todo-app/develop')
from datetime import datetime
from models.user import User
from models.post import Post, db
from test_model import TestModel
from services.post_service import PostService
import unittest

postservice = PostService(db.session)

class Test_PostService(TestModel):

    def test_get_all_posts(self):
        with self.app.app_context():
            post = postservice.get_all_posts(1)
            self.assertIsNotNone(post)
            self.assertIsInstance(post, list)
            self.assertEqual(post[0].title, "Test")
            self.assertEqual(post[0].tags[0].tag_name, "SampleTag")

    def test_create_post(self):
        with self.app.app_context():
            title = "test2"
            detail = "Test2 Detail"
            due ="2023-10-20"
            user = User.query.get(1)
            first_count = Post.query.count()
            post = postservice.create_post(title, detail, due, user)
            new_count = Post.query.count()
            self.assertIsNotNone(post)
            self.assertEqual(new_count, first_count + 1)

    def test_get_post_by_id(self):
        with self.app.app_context():
            post = postservice.get_post_by_id(1)
            self.assertIsNotNone(post)
            self.assertEqual(post.title, "Test")
            self.assertEqual(post.detail, "Test Detail")

    def test_update_post(self):
        with self.app.app_context():
            id = 1
            title = "Test re"
            detail = "Test Detail re"
            due = "2023-10-21"
            postservice.update_post(id, title, detail, due)
            post = Post.query.get(1)
            self.assertEqual(post.title, "Test re")

    def test_delete_post(self):
        with self.app.app_context():
            first_count = Post.query.count()
            id = 1
            postservice.delete_post(1)
            new_count = Post.query.count()
            self.assertEqual(new_count, first_count - 1)

if __name__ == '__main__':
    unittest.main()
