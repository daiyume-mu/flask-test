from models.user import User, db
import hashlib
import os

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed

def verify_password(stored_password, provided_password):
    salt = stored_password[:16]
    return stored_password == hash_password(provided_password, salt)

def register_user(email, password):
    hashed_pw = hash_password(password)
    new_user = User(email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user(email):
    return User.query.filter_by(email=email).first()

def get_current_user(user_id):
    if user_id:
        return User.query.filter_by(id=user_id).first()
    return None