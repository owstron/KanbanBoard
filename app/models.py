from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    passwordHash = db.Column(db.String)
    passwordSalt = db.Column(db.String)
    maxProgressLimit = db.Column(db.Integer)
    tasks = db.relationship('Task', backref='user')

    def __repr__(self):
        return '<User {}, email: {}>'.format(self.firstName, self.email)

    def set_password(self, password):
        self.passwordSalt = str(bcrypt.gensalt())
        self.passwordHash = generate_password_hash(password + self.passwordSalt)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password + self.passwordSalt)


class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.firstName = 'Guest'
    self.lastName = 'Atithi'
    self.email = 'guest@email.com'

login.anonymous_user = Anonymous

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Task(db.Model):
    __tablename__ = 'tasks'
    taskId = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.String)
    taskDesc = db.Column(db.String)
    taskStatus = db.Column(db.String, default = "ToDo")
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Task {}>'.format(self.taskName)
