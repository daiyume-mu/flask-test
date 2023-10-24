from datetime import datetime
from models.post import Post, post_user, db
from models.tag import Tag, db
from sqlalchemy import desc

class PostService:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all_posts(self, user_id):
        for post in self.db_session.query(Post).options(db.joinedload(Post.tags)).all():
            print(post)
            if post.tags:
                for tag in post.tags:
                    print(tag.tag_name)
                print(f'Post ID {post.id} has no associated tag')

        return (self.db_session.query(Post)
                 .join(post_user, Post.id == post_user.c.post_id)
                 .filter(post_user.c.user_id == user_id)
                 .options(db.joinedload(Post.tags))
                 .order_by(Post.due)
                 .all())

    def create_post(self, title, detail, due, user):
        converted_due = self.to_datetime(due)
        new_post = Post(title=title, detail=detail, due=converted_due)
        new_post.users.append(user)
        self.db_session.add(new_post)
        self.db_session.commit()
        return new_post

    def get_post_by_id(self, id):
        return self.db_session.query(Post).get(id)

    def update_post(self, id, title, detail, due):
        post = self.get_post_by_id(id)
        post.title = title
        post.detail = detail
        post.due = self.to_datetime(due)
        self.db_session.commit()
        return post

    def delete_post(self, id):
        post = self.get_post_by_id(id)
        self.db_session.delete(post)
        self.db_session.commit()

    def to_datetime(self, due):
        return datetime.strptime(due, '%Y-%m-%d')
