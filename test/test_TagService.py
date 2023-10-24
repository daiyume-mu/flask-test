import sys
sys.path.append('D:/file/flask-todo-app/develop')
from test_model import TestModel
import unittest
from models.tag import Tag, TagModel
from models.post import Post,db

tagservice = TagModel(db.session)

class Test_TagService(TestModel):
    
    def test_get_post_by_id(self):
        with self.app.app_context():
            tag_id = 1 
            user_id = 1
            posts = tagservice.get_posts_by_tag_id(tag_id, user_id)
            self.assertIsNotNone(posts)
            self.assertIsInstance(posts, list)
            self.assertEqual(posts[0].title, "Test")

    def test_create_tag(self):
        with self.app.app_context():
            first_count = Tag.query.count()
            tag = "SampleTag2"
            tagservice.create_tag(tag)
            new_count = Tag.query.count()
            self.assertEqual(new_count, first_count + 1)

    def test_get_all_tags(self):
        with self.app.app_context():
            tag = tagservice.get_all_tags()
            self.assertIsInstance(tag, list)
            self.assertEqual(tag[0].tag_name, "SampleTag")

    def test_associate_tags(self):
        with self.app.app_context():
            post = Post.query.get(1)
            tag = Tag(tag_name="SampleTag3")
            db.session.add(tag)
            db.session.commit()
            self.assertNotIn(tag, post.tags)
            tagservice.associate_tags(post, [tag.id])
            new_post = Post.query.get(1)
            self.assertIn(tag, new_post.tags)

    def test_tag_clear(self):
        with self.app.app_context():
            post = Post.query.get(1)
            self.assertTrue(post.tags)
            tagservice.tag_clear(post)
            self.assertFalse(post.tags)

if __name__ == '__main__':
    unittest.main()