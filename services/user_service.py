import bcrypt
from models.user import User, UserModel, db

class UserService:
    
    def __init__(self, repository: UserModel):
        self.repository = repository


    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed


    def verify_password(self, stored_password, provided_password):    
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


    def register_user(self, email, password):
        hashed_pw = self.hash_password(password)
        new_user = User(email=email, password=hashed_pw)
        self.repository.register_user(new_user)
        return new_user


    def get_user(self, email):
        return self.repository.get_user_by_email(email)


    def get_current_user(self, user_id):
        if user_id:
            return self.repository.get_user_by_id(user_id)
        return None
    

    def serialize_user(self, user):
        return {
            "id": user.id,
            "email": user.email
    	}