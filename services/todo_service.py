from datetime import datetime
from models.post import Post, CommentDate, db

def get_all_posts():
    return Post.query.order_by(Post.due).all()

def create_post(title, detail, due):
    convertedDue = toDatetime(due)
    new_post = Post(title=title, detail=detail, due=convertedDue)
    db.session.add(new_post)
    db.session.commit()

def get_post_by_id(id):
    return Post.query.get(id)

def toDatetime(due):
    return datetime.strptime(due, '%Y-%m-%d')

def update_post(id, title, detail, due):
    post = get_post_by_id(id)
    post.title = title
    post.detail = detail
    post.due = datetime.strptime(due, '%Y-%m-%d')
    db.session.commit()

def delete_post(id):
    post = get_post_by_id(id)
    db.session.delete(post)
    db.session.commit()

def comment_post(post_id, comment, comment_timestamp):
    new_comment = CommentDate(post_id=post_id, comment=comment, comment_timestamp=comment_timestamp)
    db.session.add(new_comment)
    db.session.commit()

"""def get_post_and_comment(id):
    post = Post.query.get(id)
    comments = post.comments
    return post, comments"""