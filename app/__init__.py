from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__) #initiating flask app
app.config.from_object(Config) # using the environment configuration to setup the app
db = SQLAlchemy(app) # connecting database to app using SQL Alchemy
migrate = Migrate(app, db) # migrating the new changes to database
login = LoginManager(app) # Integrating LoginManager for login and authentication of user
login.login_view = 'login'
login.init_app(app) # Initializing the flask app that is integrated with LoginManager

# Importing routes and models after initiating the apps.
from app import routes, models
