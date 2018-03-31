# from flask_testing import TestCase
# from flask import url_for
# from app import app, db
# from app.models import User
#
# class BaseTest(TestCase):
#     def create_app(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         self.app = app.test_client()
#         return app
#
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         self.app = app.test_client()
#         db.drop_all()
#         db.create_all()
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#
#
# class UserTests(BaseTest):
#     def test_invalid_login(self):
#         '''Login InValid User'''
#         email = 'test@test.com'
#         password = 'bluop'
#         response = self.app.post('/login', data=dict(email=email,
#             password=password), follow_redirects=True)
#         print('\n\n\n\n')
#         print(response.location)
#         self.assert_redirects(response, url_for('login'))
