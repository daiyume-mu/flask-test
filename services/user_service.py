import bcrypt
from models.user import User, db

class UserService:

    def __init__(self, db_session):
        self.db_session = db_session

    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed

    def verify_password(self, stored_password, provided_password):    
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    def register_user(self, email, password):
        hashed_pw = self.hash_password(password)
        new_user = User(email=email, password=hashed_pw)
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def get_user(self, email):
        return User.query.filter_by(email=email).first()

    def get_current_user(self, user_id):
        if user_id:
            return User.query.filter_by(id=user_id).first()
        return None
