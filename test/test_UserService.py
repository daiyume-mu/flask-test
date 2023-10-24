import sys
sys.path.append('D:/file/flask-todo-app/develop')
import bcrypt
from models.user import User
from models.post import Post, db
from services.user_service import UserService
from test_model import TestModel
import unittest

userservice = UserService(db.session)

class Test_UserService(TestModel):
    
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
            email = "test2@example.com"
            password = "password456"
            first_count = User.query.count()
            userservice.register_user(email, password)
            new_count = User.query.count()
            self.assertEqual(new_count, first_count + 1)

    def test_get_user(self):
        with self.app.app_context():
            email = "test@example.com"
            user = userservice.get_user(email)
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@example.com")
            self.assertEqual(user.password, "password123")

    def test_get_current_user(self):
        with self.app.app_context():
            user_id = 1
            user = userservice.get_current_user(user_id)
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@example.com")
            self.assertEqual(user.password, "password123")

if __name__ == '__main__':
    unittest.main()