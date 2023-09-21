from models.comment import Comment, db


def comment_post(post_id, content, content_timestamp):
    new_comment = Comment(post_id=post_id, content=content, content_timestamp=content_timestamp)
    db.session.add(new_comment)
    db.session.commit()
