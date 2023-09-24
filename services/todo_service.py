from datetime import datetime
from models.post import Post, db
from models.tag import Tag, db

def get_all_posts():
    for post in Post.query.options(db.joinedload(Post.tag)).all():
        if post.tag is not None:
            print(post.tag.tag_name)  # または logging.debug(post.tag.tag_name)
        else:
            print(f'Post ID {post.id} has no associated tag')  # または logging.warning
    
    return Post.query.options(db.joinedload(Post.tag)).all()

def create_post( title, detail, due, tag_id=None):
    convertedDue = toDatetime(due)
    new_post = Post(tag_id=tag_id, title=title, detail=detail, due=convertedDue)
    db.session.add(new_post)
    db.session.commit()

def get_post_by_id(id):
    return Post.query.get(id)

def toDatetime(due):
    return datetime.strptime(due, '%Y-%m-%d')

def update_post(id, title, detail, due, tag_id=None):
    post = get_post_by_id(id)
    post.title = title
    post.detail = detail
    post.due = datetime.strptime(due, '%Y-%m-%d')
    post.tag_id = tag_id
    db.session.commit()

def delete_post(id):
    post = get_post_by_id(id)
    db.session.delete(post)
    db.session.commit()
