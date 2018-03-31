import unittest
import flask_testing
import os
import config

from flask import url_for
from app import app, db
from app.models import User, Task

class BasicTests(unittest.TestCase):
    '''Setup and Teardown'''

    user1 = User(firstName="Test", lastName="LastTest", email="test@test.com")
    user1.set_password('testing')

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ''' Tests'''

    def test_main_page(self):
        '''Testing Homepage'''
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_page(self):
        '''Testing Invalid page'''
        response = self.app.get('/random', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_add_new_user(self):
        '''Adding New User'''
        db.session.add(self.user1)
        db.session.commit()

    def test_valid_login(self):
        '''Login Valid User'''
        email = 'test@test.com'
        password = 'testing'
        response = self.app.post('/login', data=dict(email=email,
            password=password), follow_redirects=True)
        print('\n\n\n\n')
        print(response.location)
        self.assertEqual(response.status_code, 200) #Redirected after login to another page.

    def test_invalid_login(self):
        '''Login InValid User'''
        email = 'test@test.com'
        password = 'bluop'
        response = self.app.post('/login', data=dict(email=email,
            password=password), follow_redirects=True)
        print('\n\n\n\n')
        print(response.location)
        self.assertEqual(response.status_code, 200)
        # self.assert_redirects(response, url_for('login'))

if __name__ == "__main__":
    unittest.main()
