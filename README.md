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
** To prepare the database and run the app **
The `flask db init` commands gives `alembic.util.exc.CommandError: Directory migrations already exists` error.

It can be neglected as we have to create an empty `kanban.db` since it is not uploaded with the package.
```
$ export FLASK_APP=kanban.py
$ rm kanban.db
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask run

```

### How to run unit tests?
The unit tests are in `./app/tests/` folder.
```
$ python3 -m unittest discover -v
```
