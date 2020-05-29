import unittest
from main import app
import os
import json

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
            data=dict(username=username, password=password,genre=genre),
            follow_redirects=True
        )
    # DONE USER REGISTRATION CHECK
    # def test_valid_user_registration(self):
    #     response = self.register('gambhir', 'gambhir','Horror|Comedy')
    #     self.assertEqual(response.status,'200 OK')

    # DONE USER REGISTRATION CHECK
    def test_invalid_user_registration_different_passwords(self):
        response = self.register('kashish', 'sagar','Horror|Comedy')
        print(response.data['message'])
        self.assertEqual(data['status'],300)

if __name__ == "__main__":
    unittest.main()
 