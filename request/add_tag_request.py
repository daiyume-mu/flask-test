from models.tag import Tag, db

def is_unique_tag(tag_name):
    existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
    return existing_tag is None