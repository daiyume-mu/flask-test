from models.user import User

def is_unique_user(email):
    existing_user = User.query.filter_by(email=email).first()
    return existing_user is None