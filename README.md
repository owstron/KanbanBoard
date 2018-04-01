# KanbanBoard

This app is available at <https://www.github.com/nik1997/kanbanboard>

## How to use this app?
### Follow the following commands:
** To install all the dependencies: **
```
$ python3.6 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```
** To run the app **
```
$ export FLASK_APP=kanban.py
$ flask run
```

There are not default users, so please start by creating a new user. :blush:

### How to run unit tests?
The unit tests are in `./app/tests/` folder.
```
$ python3 -m unittest discover -v
```
