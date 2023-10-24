"""from models.tag import Tag, db
from models.post import Post,post_tag, post_user, db
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

class TagService:

    def __init__(self, db_session):
        self.db_session = db_session

    def get_posts_by_tag_id(self, tag_id, user_id):
        posts = (self.db_session.query(Post)
                 .join(Post.tags)
                 .join(post_user, Post.id == post_user.c.post_id)
                 .filter(Tag.id == tag_id, post_user.c.user_id == user_id)
                 .options(joinedload(Post.tags))
                 .order_by(Post.due)
                 .all())
        return posts

    def create_tag(self, tag):
        new_tag = Tag(tag_name=tag)
        self.db_session.add(new_tag)
        self.db_session.commit()
        return new_tag

    def get_all_tags(self):
        return Tag.query.all()

    def associate_tags(self, post, tag_id):
        tags = Tag.query.filter(Tag.id.in_(tag_id)).all()
        post.tags.extend(tags)
        self.db_session.commit()
        print(tags)

    def tag_clear(self, post):
        if post.tags:
            post.tags.clear()"""

#associateするだけの関数を作る
#addするだけの関数を作る
#modelのりファクタは後で教えるからいい