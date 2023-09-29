from datetime import datetime
from models.post import Post, db
from models.tag import Tag, db
from sqlalchemy import desc

def get_all_posts():
    """for post in Post.query.options(db.joinedload(Post.tags)).all():
        if post.tag is not None:
            print(post.tag.tag_name)  
        else:
            print(f'Post ID {post.id} has no associated tag')"""
    
    return Post.query.options(db.joinedload(Post.tags)).order_by((Post.due)).all()

def create_post( title, detail, due):
    convertedDue = toDatetime(due)
    new_post = Post(title=title, detail=detail, due=convertedDue)
    db.session.add(new_post)
    db.session.commit()
    return new_post

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
    return post

def delete_post(id):
    post = get_post_by_id(id)
    db.session.delete(post)
    db.session.commit()

"""def create_posttag(post_id, tag_id):
    new_posttag = PostTag(post_id=post_id, tag_id=tag_id)
    db.session.add(new_posttag)
    db.session.commit()"""