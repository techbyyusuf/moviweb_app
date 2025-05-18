import os
import pytest
from app import create_app
from data_managers.data_manager_sqlite import SQLiteDataManager
from utils.extensions import db
from models.movie import Movie
from models.user import User
from sqlalchemy import select

TEST_DB = os.path.abspath("tests/test.db")
TEST_DB_URI = f'sqlite:///{TEST_DB}'


@pytest.fixture(scope='function', autouse=True)
def test_app_context():
    app = create_app(TEST_DB_URI)

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield


def test_db_file_created(test_app_context):
    assert os.path.exists(TEST_DB)

def test_users_movies_table_exists(test_app_context):
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "movies" in tables



def test_add_user(test_app_context):
    data_manager = SQLiteDataManager()
    data_manager.add_user('Frank')

    users = db.session.scalars(select(User)).all()
    assert any(user.name == 'Frank' for user in users)



def test_delete_user(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')

    users = db.session.scalars(select(User)).all()
    assert any(user.name == 'TestUser1' for user in users)

    user_id = users[0].user_id
    data_manager.delete_user(user_id)

    users = db.session.scalars(select(User)).all()
    assert all('TestUser1' != user.name for user in users)


def test_get_all_users(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    data_manager.add_user('TestUser2')

    users = data_manager.get_all_users()

    assert isinstance(users, list)
    assert len(users) >= 2
    assert any('TestUser1' == user.name for user in users)
    assert any('TestUser2' == user.name for user in users)


def test_add_movie(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.scalars(select(User)).all()

    user_id = users[0].user_id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)

    movie = db.session.get(Movie, 1)

    assert movie.title == 'Titanic'
    assert movie.director == 'Di Caprio'
    assert movie.year == 1997
    assert movie.rating == 9.9
    assert movie.user_id == user_id


def test_get_user_movies(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser')
    users = db.session.scalars(select(User)).all()
    user_id = users[0].user_id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)
    data_manager.add_movie(user_id, '22 Jump Street', 'De Niro', 2010, 9.2)

    movies = data_manager.get_user_movies(user_id)

    assert isinstance(movies, list)
    assert len(movies) >= 2
    assert any('Titanic' == movie.title for movie in movies)
    assert any('22 Jump Street' == movie.title for movie in movies)


def test_delete_movie(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')

    users = db.session.scalars(select(User)).all()
    user_id = users[0].user_id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)

    data_manager.delete_movie(1,user_id)

    movies = db.session.scalars(select(Movie)).all()

    assert all('Titanic' != movie.title for movie in movies)


def test_update_movie(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.scalars(select(User)).all()
    user_id = users[0].user_id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)
    movies = db.session.scalars(select(Movie)).all()

    assert any('Titanic' == movie.title for movie in movies)

    update_movie = Movie(
        movie_id = 1,
        title= 'Updated title',
        director='Updated director',
        year=2024,
        rating=0.5
    )

    data_manager.update_movie(update_movie)

    updated_movie = db.session.get(Movie, 1)
    assert updated_movie.title == 'Updated title'
    assert updated_movie.director == 'Updated director'
    assert updated_movie.year == 2024
    assert updated_movie.rating == 0.5


def test_get_movie_by_id(test_app_context):
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.scalars(select(User)).all()
    user_id = users[0].user_id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)
    movie = data_manager.get_movie_by_id(1)

    assert movie is not None
    assert isinstance(movie, Movie)
    assert 'Titanic' == movie.title
    assert 'Di Caprio' == movie.director