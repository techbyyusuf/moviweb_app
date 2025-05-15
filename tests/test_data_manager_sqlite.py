import sys
import os

from pydantic_core.core_schema import is_instance_schema

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
from sqlalchemy import select

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
    data_manager.add_user('Frank')

    users = db.session.query(User).all()
    data_manager.delete_user(1)

    assert any(user.name == 'Frank' for user in users)



def test_delete_user(test_app_context):
    data_manager = SQLiteDataManager()

    users = db.session.query(User).all()
    if not users:
        data_manager.add_user('TestUser1')

    data_manager.delete_user(1)

    users = db.session.query(User).all()
    assert 1 not in [user.id for user in users]



def test_get_all_users(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    data_manager.add_user('TestUser2')

    users = data_manager.get_all_users()

    assert isinstance(users, list)
    assert len(users) >= 2
    assert 'TestUser1' in users
    assert 'TestUser2' in users

    for user in users:
        user_obj = db.session.scalar(select(User).where(User.name == user))
        if user_obj:
            data_manager.delete_user(user_obj.id)


def test_add_user_movie(test_app_context):
    data_manager = SQLiteDataManager()

    users = db.session.query(User).all()
    if not users:
        data_manager.add_user('TestUser1')
        users = db.session.query(User).all()

    user_id = users[0].id

    data_manager.add_user_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)

    movies = db.session.query(Movie).all()

    assert any(movie.name == 'Titanic' for movie in movies)
    assert (movie.user_id == user_id for movie in movies)

    data_manager.delete_user_movie(1)

def test_get_user_movies(test_app_context):
    data_manager = SQLiteDataManager()

    user = db.session.query(User).first()

    data_manager.add_user_movie(user.id, 'Titanic', 'Di Caprio', 1997, 9.9)
    data_manager.add_user_movie(user.id, '22 Jump Street', 'De Niro', 2010, 9.2)

    movies = data_manager.get_user_movies(user.id)

    assert isinstance(movies, list)
    assert len(movies) >= 2
    assert any('Titanic' in movie.name for movie in movies)
    assert any('22 Jump Street' in movie.name for movie in movies)


def test_delete_user_movie(test_app_context):
    data_manager = SQLiteDataManager()

    users = db.session.query(User).all()
    if not users:
        data_manager.add_user('TestUser1')

    user_id = users[0].id

    movies = db.session.query(Movie).all()
    if not movies:
        data_manager.add_user_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)

    data_manager.delete_user_movie(2)

    movies = db.session.query(Movie).all()

    assert ('Titanic' == movie.name for movie in movies)