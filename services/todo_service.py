from datetime import datetime
from models.post import Post, db

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
