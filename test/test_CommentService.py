import sys
sys.path.append('D:/file/flask-todo-app/develop')
from datetime import datetime
from models.comment import Comment
from models.post import db
from services.comment_service import CommentService
from test_model import TestModel
import unittest


commentservice = CommentService(db.session)

class Test_CommentService(TestModel):

    def test_comment_post(self):
        with self.app.app_context():
            post_id = 1 
            content = "test comment2"
            comment_time = datetime.now()
            first_count = Comment.query.filter_by(post_id=post_id).count()
            commentservice.comment_post(post_id, content, comment_time)
            new_count = Comment.query.filter_by(post_id=post_id).count()
            self.assertEqual(new_count, first_count + 1)

if __name__ == '__main__':
    unittest.main()
