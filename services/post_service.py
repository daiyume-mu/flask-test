from datetime import datetime
from models.post import Post,PostModel, post_user, db
from models.tag import Tag, db
from sqlalchemy import desc

class PostService:
    
    def __init__(self, repository: PostModel):
        self.repository = repository


    def get_all_posts(self, user_id):
        """for post in self.db_session.query(Post).options(db.joinedload(Post.tags)).all():
            print(post)
            if post.tags:
                for tag in post.tags:
                    print(tag.tag_name)
                print(f'Post ID {post.id} has no associated tag')"""

        return self.repository.get_all_posts(user_id)
    

    def create_post(self, title, detail, due):
        converted_due = self.to_datetime(due)
        new_post = Post(title=title, detail=detail, due=converted_due)
        self.repository.add_post(new_post)
        return new_post


    def associate_user(self, post, user):
        self.repository.associate_user(post, user)
        

    def get_post_by_id(self, id):
        return self.repository.get_post_by_id(id)


    def update_post(self, id, title, detail, due):
        post = self.repository.get_post_by_id(id)
        post.title = title
        post.detail = detail
        post.due = self.to_datetime(due)
        self.repository.update_post(post)        
        return post


    def delete_post(self, id):
        self.repository.delete_post_by_id(id)


    def to_datetime(self, due):
        return datetime.strptime(due, '%Y-%m-%d')
    

    def serialize_post(self, post):
        return {
            "id": post.id,
            "title": post.title,
            "detail": post.detail,
            "due": post.due.strftime('%Y-%m-%d %H:%M:%S'),
            "user": {
                "id": post.user.id,
                "email": post.user.email  # ユーザーモデルの他の属性もここに追加できます。
            },
            "tags": [{
                "id": tag.id,
                "tag_name": tag.tag_name  # タグモデルの他の属性もここに追加できます。
            } for tag in post.tags],
            "comments": [{
                "id": comment.id,
                "post_id": comment.post_id,
                "content": comment.content,
                "content_timestamp": comment.content_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } for comment in post.comments]
        }
