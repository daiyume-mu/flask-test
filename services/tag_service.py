from models.tag import Tag, db
from models.post import Post,post_tag, post_user, db
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

def get_posts_by_tag_id(tag_id, user_id):
    posts = posts = (Post.query
             .join(Post.tags)
             .join(post_user, Post.id == post_user.c.post_id)
             .filter(Tag.id == tag_id, post_user.c.user_id == user_id)
             .options(joinedload(Post.tags))
             .order_by(Post.due)
             .all())
    return posts

def create_tag(tag):
    new_tag = Tag(tag_name=tag)
    db.session.add(new_tag)
    db.session.commit()
    return new_tag

def get_all_tags():
    return Tag.query.all()

def associate_tags(post, tag_id):
    tags = Tag.query.filter(Tag.id.in_(tag_id)).all()
    post.tags.extend(tags)
    db.session.commit()
    print(tags)

def tag_clear(post):
    if post.tags:
        post.tags.clear()


#associateするだけの関数を作る
#addするだけの関数を作る
#modelのりファクタは後で教えるからいい