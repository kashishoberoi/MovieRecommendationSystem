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
        self.assertEqual(app.debug, False)

    def login(self,username, password):
        return self.app.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True
        )
    def logout(self):
        return self.app.get(
            '/userlogout',
            follow_redirects=True
        )
 
    def register(self, username, password,genre):
        return self.app.post(
            '/signup',
            data=dict(username=username, password=password,genre=genre),
            follow_redirects=True
        )
    def searchGen(self,username,search_string):
        return self.app.post(
            '/searchgenre',
            data=dict(username=username, search_string = search_string),
            follow_redirects=True
        )
    def searchMovie(self,username,search_string):
        return self.app.post(
            '/searchmovie',
            data=dict(username=username, search_string = search_string),
            follow_redirects=True
        )
        # userratingpage
    def loadUserRatingPage(self,username):
        return self.app.post(
            '/userratingpage',
            data=dict(username=username),
            follow_redirects=True
        )
    def updateRating(self,username,movieId,rating):
        return self.app.post(
            '/updaterating',
            data=dict(username=username,movieId=movieId,user_rating=rating),
            follow_redirects=True
        )
    # Valid User signup check
    def test_valid_user_registration(self):
        response = self.register('newbie', 'newbie','Horror|Comedy')
        self.assertEqual(response.status,'200 OK')

    # Invalid User signup check
    def test_invalid_user_registration_different_passwords(self):
        response = self.register('kashish', 'sagar','Horror|Comedy')
        self.assertIn(response.status,'401 UNAUTHORIZED')

    # Invalid login check
    def test_invalid_login(self):
        response = self.login('mroberoi', 'mraditya')
        self.assertEqual(response.status,'401 UNAUTHORIZED')

    #Valid Login check
    def test_valid_login(self):
        response = self.login('mroberoi', 'mroberoi')
        self.assertEqual(response.status,'200 OK')

    # Valid search genre
    def test_valid_searchGenre(self):
        response = self.searchGen('oberoi','Horror')
        self.assertEqual(response.status,'200 OK')
    
    #Invalid Search genre
    def test_invalid_searchGenre(self):
        response = self.searchGen('oberoi','')
        self.assertEqual(response.status,'204 NO CONTENT')

    # Valid search movie
    def test_valid_searchMovie(self):
        response = self.searchMovie('oberoi','Love')
        self.assertEqual(response.status,'200 OK')
    
    #Invalid Search movie
    def test_invalid_searchMovie(self):
        response = self.searchMovie('oberoi','')
        self.assertEqual(response.status,'204 NO CONTENT')

    #Valid user Rating page Loaded
    def test_valid_userRatingPage(self):
        response = self.loadUserRatingPage('sagar')
        self.assertEqual(response.status,'200 OK')

    #invalid user Rating Page loaded
    def test_invalid_userRatingPage(self):
        response = self.loadUserRatingPage('gambhir')
        self.assertEqual(response.status,'204 NO CONTENT')

    #Valid User rating update
    def test_valid_userRating(self):
        response = self.updateRating('sagar',13,4.5)
        self.assertEqual(response.status,'200 OK')

    #invalid user Rating update
    def test_invalid_userRating(self):
        response = self.updateRating('sagar123',12,4.5)
        self.assertEqual(response.status,'401 UNAUTHORIZED')

    #valid logout
    def logoutUser(self):
        response = self.logout('sagar')
        self.assertEqual(response.status,'200 OK')

if __name__ == "__main__":
    unittest.main()
 