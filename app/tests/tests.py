import os
import config
import unittest

from flask import url_for
from app import app, db
from app.models import User, Task
from flask_login import login_user, logout_user, current_user

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
        app.config['LOGIN_DISABLED'] = False
        self.client = app.test_client()
        db.drop_all()
        db.create_all()
        self.create_user()

    # executed after each test
    def tearDown(self):
        db.drop_all()


    ########################
    #### helper methods ####
    ########################

    def register(self, firstName, lastName, maxProgressLimit, email, password, password2):
        return self.client.post(
            '/register',
            data=dict(firstName=firstName, lastName=lastName, maxProgressLimit = maxProgressLimit, email=email, password=password, password2=password2),
            follow_redirects=True
        )

    def login(self, email, password, remember_me):
        return self.client.post(
            '/login',
            data=dict(email=email, password=password, remember = remember_me),
            follow_redirects=True
        )

    def logout(self):
        return self.client.get(
            '/logout',
            follow_redirects=True
        )

    def create_user(self):
        test_user = User(firstName='Nikesh', lastName='Shrestha', \
            maxProgressLimit = 3, email='nikesh@email.com')
        test_user.set_password('FlaskIsAwesome')
        db.session.add(test_user)
        db.session.commit()
        self.test_user = test_user

    def login_test_user(self):
        '''Logs in a user for testing purposes'''
        return self.client.post(
            '/login',
            data=dict(email='nikesh@email.com', password='FlaskIsAwesome', remember_me = False),
            follow_redirects=True
        )

    ########################
    #### Test Pages     ####
    ########################

    def test_main_page(self):
        '''Test existence of index page'''
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_page(self):
        '''Test existence of Invalid Page'''
        response = self.client.get('/random', follow_redirects=True)
        self.assertEqual(response.status_code, 404)


    #########################
    ##### Test pages without login
    #########################
    def test_delete_without_login(self):
        '''Test delete page access leads to login page if not logged in'''
        response = self.client.get('/delete_all', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In - Kanban Board', response.data)

    def test_add_without_login(self):
        '''Test add page without login'''
        response = self.client.post('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In - Kanban Board', response.data)


    ########################
    #### Test User Registration    ####
    ########################

    def test_valid_user_registration(self):
        '''Test valid user registration'''
        response = self.register('Nikesh', 'Shrestha',3, 'nikesh@minerva.kgi.edu','FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In - Kanban Board', response.data)

    def test_invalid_user_registration_missing_name(self):
        '''Test user registration with missing name'''
        response = self.register('', 'Shrestha',3, 'nikesh@email.com','FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)

    def test_invalid_user_registration_wrong_confirmation_password(self):
        '''Test user registration with wrong confirmation password'''
        response = self.register('Philip', 'Sterne',3, 'sterny@tesla.com','FlaskIsAwesome', 'FlaskIsNotAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_invalid_user_registration_used_email(self):
        '''Test user registration with already used email'''
        response = self.register('Philip', 'Sterne',3, 'nikesh@email.com','FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please use a different email.', response.data)


    ########################
    #### Test Login
    ########################

    def test_valid_login(self):
        '''Test Valid Login'''
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email='nikesh@email.com', password='FlaskIsAwesome', remember_me = False),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Welcome', response.data)

    def test_invalid_login_no_email(self):
        '''Test Invalid Login without email'''
        response = self.client.post(
            '/login',
            data=dict(email='', password='FlaskIsAwesome', remember_me = False),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_login_no_password(self):
        '''Test login without password'''
        response = self.client.post(
            '/login',
            data=dict(email='nikesh@email.com', password='', remember_me = False),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_login_wrong_email(self):
        '''Test login with wrong email'''
        response = self.client.post(
            '/login',
            data=dict(email='wrongemail', password='FlaskIsAwesome', remember_me = False),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_login_wrong_password(self):
        '''Test login with wrong password'''
        response = self.client.post(
            '/login',
            data=dict(email='nikesh@email.com', password='WrongPassword', remember_me = False),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)



    ########################
    ######## Test pages after login
    ########################

    def logout(self):
        '''Testing logout'''
        with self.client:
            resp_login = self.login_test_user()
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sign In - KanbanBoard', response.data)


    def test_add(self):
        '''Testing adding new item'''
        with self.client:
            resp_login = self.login_test_user()
            response = self.client.post('/add',
                        data=dict(taskitem='CS162'),
                        follow_redirects=True)
            task = Task.query.filter_by(taskName='CS162').first()
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'CS162', response.data)
            self.assertEqual(task.taskName, 'CS162')

    def test_move_to_progress(self):
        '''Test moving already saved stuff to progress'''
        with self.client:
            resp_login = self.login_test_user()
            response2 = self.client.post('/add',
                        data=dict(taskitem='CS162'),
                        follow_redirects=True)
            response = self.client.get('/progress/1',
                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Mark as Done', response.data)
            task = Task.query.filter_by(taskName='CS162').first()
            self.assertEqual(task.taskStatus, 'Progress')

    def test_move_to_done(self):
        '''Test moving already saved stuff to done'''
        with self.client:
            resp_login = self.login_test_user()
            response2 = self.client.post('/add',
                        data=dict(taskitem='CS162'),
                        follow_redirects=True)
            response = self.client.get('/done/1',
                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            task = Task.query.filter_by(taskName='CS162').first()
            self.assertEqual(task.taskStatus, 'Done')

    def test_move_to_todo(self):
        '''Test moving already saved stuff to ToDo from other place'''
        with self.client:
            resp_login = self.login_test_user()
            response2 = self.client.post('/add',
                        data=dict(taskitem='CS162'),
                        follow_redirects=True)
            # Moving the task to Done Board
            response_done = self.client.get('/done/1',
                        follow_redirects=True)
            task = Task.query.filter_by(taskName='CS162').first()
            self.assertEqual(task.taskStatus, 'Done')
            # Moving back to ToDo
            response = self.client.get('/todo/1',
                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            task = Task.query.filter_by(taskName='CS162').first()
            self.assertEqual(task.taskStatus, 'ToDo')

    def test_delete(self):
        with self.client:
            resp_login = self.login_test_user()
            # adding the task first
            response_add = self.client.post('/add',
                        data=dict(taskitem='CS162'),
                        follow_redirects=True)

            # Querying the task for checking existence
            task = Task.query.filter_by(taskName='CS162').first()
            self.assertEqual(task.taskName, 'CS162')

            # Deleteing the task
            response = self.client.get('/delete/1',
                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            task = Task.query.filter_by(taskName='CS162').first()
            self.assertEqual(task, None)


if __name__ == "__main__":
    unittest.main()
