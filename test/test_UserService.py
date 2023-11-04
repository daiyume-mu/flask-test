import sys
sys.path.append('D:/file/flask-todo-app/develop')
import bcrypt
from flask import Flask
from datetime import datetime
from models.post import Post, db
from models.comment import Comment
from models.tag import Tag
from models.user import User
from services.user_service import UserService
import unittest

userservice = UserService(db.session)

class Test_UserService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_hash_password(self):
        password = "test_password"
        hashed_password = userservice.hash_password(password)
        self.assertIsInstance(hashed_password, bytes)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password))


    def test_verify_password(self):
        original_password = "test_password"
        hashed_password = userservice.hash_password(original_password)
        self.assertTrue(userservice.verify_password(hashed_password, original_password))
        wrong_password = "wrong_password"
        self.assertFalse(userservice.verify_password(hashed_password, wrong_password))


    def test_register_user(self):
        with self.app.app_context():
            email = "test2example.com"
            password = "password123"
            first_count = User.query.count()
            userservice.register_user(email, password)
            new_count = User.query.count()
            self.assertEqual(new_count, first_count + 1)

            db.session.rollback()


    def test_get_user(self):
        with self.app.app_context():
            email = "test@example.com"
            password = "password123"
            userservice.register_user(email, password)
            
            user = userservice.get_user(email)
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@example.com")
            self.assertTrue(userservice.verify_password(user.password, password))

            db.session.rollback()


    def test_get_current_user(self):
        with self.app.app_context():
            email = "test@example.com"
            password = "password123"
            userservice.register_user(email, password)
            
            user_id = 1
            user = userservice.get_current_user(user_id)
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@example.com")
            self.assertTrue(userservice.verify_password(user.password, password))

            db.session.rollback()

if __name__ == '__main__':
    unittest.main()