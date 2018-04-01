from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Task

@app.route('/')
@app.route('/index')
@login_required
def index():
    tasks_todo = []
    tasks_progress = []
    tasks_done = []
    if current_user.is_authenticated:
        tasks_todo = Task.query.filter_by(taskStatus='ToDo').filter_by(userId = current_user.id)
        tasks_progress = Task.query.filter_by(taskStatus='Progress').filter_by(userId = current_user.id)
        tasks_done = Task.query.filter_by(taskStatus='Done').filter_by(userId = current_user.id)
    return render_template('index.html', title='Home Page', tasks_todo=tasks_todo, tasks_progress=tasks_progress, tasks_done=tasks_done)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            flash('Welcome')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(firstName=form.firstName.data,
                lastName=form.lastName.data,
                email=form.email.data,
                maxProgressLimit=form.maxProgressLimit.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/add', methods=['POST'])
@login_required
def add():
    task = Task(taskName=request.form['taskitem'], taskStatus='ToDo', userId = current_user.id)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/todo/<id>')
@login_required
def todo(id):
    task = Task.query.filter_by(taskId = int(id)).first()
    task.taskStatus = 'ToDo'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/progress/<id>')
@login_required
def progress(id):
    task = Task.query.filter_by(taskId = int(id)).first()
    task.taskStatus = 'Progress'
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/done/<id>')
@login_required
def done(id):
    task = Task.query.filter_by(taskId = int(id)).first()
    task.taskStatus = 'Done'
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete_all')
@login_required
def delete_all():
    tasks = Task.query.filter_by(taskStatus='Done')
    for task in tasks:
        db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<id>')
@login_required
def delete(id):
    task = Task.query.filter_by(taskId = int(id)).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))
