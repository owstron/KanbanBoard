import os
import config
import unittest

from flask import url_for
from app import app, db
from app.models import User, Task

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(config.basedir, TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass


    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ########################
    #### helper methods ####
    ########################

    def register(self, firstName, lastName, maxProgressLimit, email, password, password2):
        return self.app.post(
            '/register',
            data=dict(firstName=firstName, lastName=lastName, maxProgressLimit = maxProgressLimit, email=email, password=password, password2=password2),
            follow_redirects=True
        )

    def login(self, email, password, remember_me):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password, remember = remember_me),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

    def test_invalid_user_registration(self):
        response = self.register('', 'Shrestha',3, 'nikesh@email.com','FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)

    def test_valid_user_registration(self):
        response = self.register('Nikesh', 'Shrestha',3, 'nikesh@email.com','FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In - Kanban Board', response.data)

    def test_delete(self):
        response = self.app.get('/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In - Kanban Board', response.data)

    def test_valid_login(self):
        # response = self.login('nikesh@email.com', 'FlaskIsAwesome', False)
        response = self.app.post(
            '/login',
            data=dict(email='nikesh@email.com', password='FlaskIsAwesome', remember_me = False),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)



if __name__ == "__main__":
    unittest.main()
