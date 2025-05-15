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


@pytest.fixture(scope='function', autouse=True)
def test_app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.drop_all()
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
    assert any(user.name == 'Frank' for user in users)



def test_delete_user(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')

    users = db.session.query(User).all()
    assert any(user.name == 'TestUser1' for user in users)

    data_manager.delete_user(1)

    users = db.session.query(User).all()
    assert all('TestUser1' != user.name for user in users)


def test_get_all_users(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    data_manager.add_user('TestUser2')

    users = data_manager.get_all_users()

    assert isinstance(users, list)
    assert len(users) >= 2
    assert 'TestUser1' in users
    assert 'TestUser2' in users


def test_add_movie(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.query(User).all()

    user_id = users[0].id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)

    movie = db.session.get(Movie, 1)

    assert movie.name == 'Titanic'
    assert movie.director == 'Di Caprio'
    assert movie.year == 1997
    assert movie.rating == 9.9
    assert movie.user_id == user_id


def test_get_user_movies(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser')
    users = db.session.query(User).all()
    user_id = users[0].id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)
    data_manager.add_movie(user_id, '22 Jump Street', 'De Niro', 2010, 9.2)

    movies = data_manager.get_user_movies(user_id)

    assert isinstance(movies, list)
    assert len(movies) >= 2
    assert any('Titanic' == movie.name for movie in movies)
    assert any('22 Jump Street' == movie.name for movie in movies)


def test_delete_movie(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')

    users = db.session.query(User).all()
    user_id = users[0].id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)

    data_manager.delete_movie(1,user_id)

    movies = db.session.query(Movie).all()

    assert all('Titanic' != movie.name for movie in movies)


def test_update_movie(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.query(User).all()
    user_id = users[0].id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)
    movies = db.session.query(Movie).all()

    assert any('Titanic' == movie.name for movie in movies)

    update_movie = Movie(
        movie_id = 1,
        name= 'Updated title',
        director='Updated director',
        year=2024,
        rating=0.5
    )

    data_manager.update_movie(update_movie)

    updated_movie = db.session.get(Movie, 1)
    assert updated_movie.name == 'Updated title'
    assert updated_movie.director == 'Updated director'
    assert updated_movie.year == 2024
    assert updated_movie.rating == 0.5
