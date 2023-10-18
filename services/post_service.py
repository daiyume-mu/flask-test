from datetime import datetime
from models.post import Post, post_user, db
from models.tag import Tag, db
from sqlalchemy import desc

def get_all_posts(user_id):
    for post in Post.query.options(db.joinedload(Post.tags)).all():
        print(post)
        if post.tags:
            for tag in post.tags:
                print(tag.tag_name)
            print(f'Post ID {post.id} has no associated tag')
    
    return (Post.query
         .join(post_user, Post.id == post_user.c.post_id) # post_userを直接使用
         .filter(post_user.c.user_id == user_id)
         .options(db.joinedload(Post.tags))
         .order_by(Post.due)
         .all())
def create_post(title, detail, due, user):
    convertedDue = toDatetime(due)
    new_post = Post(title=title, detail=detail, due=convertedDue)
    new_post.users.append(user)
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