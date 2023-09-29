from models.tag import Tag, db
from models.post import Post,post_tag, db
from sqlalchemy import desc

def create_tag(tag_name):
    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    if not existing_tag is None:
        return existing_tag
    else:
        new_tag = Tag(tag_name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

def update_tag(post, tag_name):
    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    
    if existing_tag is not None:
        post.tags.append(existing_tag)
    else:
        new_tag = Tag(tag_name=tag_name)
        db.session.add(new_tag)
        post.tags.append(new_tag)
    
    db.session.commit()
    
def get_posts_by_tag_id(tag_id):
    posts = Post.query.options(db.joinedload(Post.tags)).order_by((Post.due)).all()
    return posts

def tag_clear(post):
    if post.tags:
        post.tags.clear()