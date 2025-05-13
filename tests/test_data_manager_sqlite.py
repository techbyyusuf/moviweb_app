import sys
import os

# absoluter Pfad zum Projektverzeichnis (eine Ebene über "tests/")
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Projektverzeichnis zu sys.path hinzufügen
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pytest
from models.user import User
from models.movie import Movie
from flask_sqlalchemy import SQLAlchemy
from data_managers.data_manager_sqlite import SQLiteDataManager
from data_managers.data_manager_interface import DataManagerInterface
from main import create_app, db

file_path = os.path.abspath("tests/test.db")
sqlite_uri = f'sqlite:///{file_path}'
app = create_app(sqlite_uri)


@pytest.fixture(scope='module')
def test_app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        from models.user import User
        from models.movie import Movie
        db.create_all()
        yield


def test_db_file_created(test_app_context):
    assert os.path.exists(file_path)

def test_users_movies_table_exists(test_app_context):
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "movies" in tables



def test_add_user(test_app_context):
    data_manager = SQLiteDataManager()
    data_manager.add_user('Alice')

    users = db.session.query(User).all()
    assert len(users) == 1
    assert users[0].name == 'Alice'


def test_delete_user(test_app_context):
    data_manager = SQLiteDataManager()

    user = User(id=1, name="TestUser")
    db.session.add(user)
    db.session.commit()

    data_manager.delete_user(1)
    users = db.session.query(User).all()
    assert 1 not in [user.id for user in users]


def test_get_all_users():
    pass