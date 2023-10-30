from models.tag import Tag, TagModel, db
from models.post import Post,post_tag, post_user, db
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

class TagService:
    
    def __init__(self, repository: TagModel):
        self.repository = repository


    def get_posts_by_tag_id(self, tag_id, user_id):
        return self.repository.get_posts_by_tag_id(tag_id, user_id)


    def create_tag(self, tag):
        new_tag = Tag(tag_name=tag)
        self.repository.add_tag(new_tag)
        return new_tag


    def get_all_tags(self):
        return self.repository.get_all_tags()


    def associate_tags(self, post, tag_id):
        self.repository.associate_tags(post, tag_id)


    def tag_clear(self, post):
        self.repository.tag_clear(post)

#associateするだけの関数を作る
#addするだけの関数を作る
#modelのりファクタは後で教えるからいい