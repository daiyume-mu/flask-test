from models.comment import Comment

class CommentService:

    def __init__(self, db_session):
        self.db_session = db_session

    def comment_post(self, post_id, content, content_timestamp):
        new_comment = Comment(post_id=post_id, content=content, content_timestamp=content_timestamp)
        self.db_session.add(new_comment)
        self.db_session.commit()

