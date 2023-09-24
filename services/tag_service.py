from models.tag import Tag, db
from models.post import Post, db

def create_tag(tag_name):
    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    if not existing_tag is None:
        return existing_tag
    else:
        new_tag = Tag(tag_name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

def update_tag(tag_name):
    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    if not existing_tag is None:
        return existing_tag
    else:
        new_tag = Tag(tag_name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag
    
def get_posts_by_tag_id(tag_id):
    return Post.query.filter(Post.tag_id == tag_id).all()