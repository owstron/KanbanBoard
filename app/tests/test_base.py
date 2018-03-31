# # flask_testing/test_base.py
# from flask_testing import TestCase
#
# import os
# import config
# from app import app, db
#
#
# class BaseTestCase(TestCase):
#     """A base test case for flask-tracking."""
#
#     def create_app(self):
#         app.config.from_object('config.TestConfiguration')
#         return app
#
#     def setUp(self):
#         app.config.from_object('config.TestConfiguration')
#         self.app = app.test_client()
#         db.create_all()
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
