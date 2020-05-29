import unittest
from main import app
import os

TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join('./', TEST_DB)
        self.app = app.test_client()
        # db.drop_all()
        # db.create_all()
        self.assertEqual(app.debug, False)

    def login(username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )
    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )
 
    def register(self, username, password,genre):
        return self.app.post(
            '/signup',
            data=dict(username=username, password=password,genre),
            follow_redirects=True
        )
    def test_valid_user_registration(self):
        response = self.register('gambhir', 'gambhir','Horror|Comedy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thanks for registering!', response.data)

    def test_invalid_user_registration_different_passwords(self):
        response = self.register('kashish', 'sagar')
        self.assertIn(b'user already there', response.data)

if __name__ == "__main__":
    unittest.main()
 