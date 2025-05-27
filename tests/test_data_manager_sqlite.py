import os
from sqlalchemy import select
from datetime import datetime

import pytest

from app import create_app
from data_managers.data_manager_sqlite import SQLiteDataManager
from models.movie import Movie
from models.user import User
from utils.extensions import db

TEST_DB = os.path.abspath("tests/test.db")
TEST_DB_URI = f'sqlite:///{TEST_DB}'


@pytest.fixture(scope='function', autouse=True)
def test_app_context():
    """Provide a fresh app context and database for each test."""
    app = create_app(TEST_DB_URI)

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield


def test_db_file_created(test_app_context):
    """Check that the test database file is created."""
    assert os.path.exists(TEST_DB)


def test_users_movies_table_exists(test_app_context):
    """Check that 'users' and 'movies' tables exist in the DB."""
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "movies" in tables


def test_add_user(test_app_context):
    """Test adding a user to the database."""
    data_manager = SQLiteDataManager()
    data_manager.add_user('Frank')

    users = db.session.scalars(select(User)).all()
    assert any(user.name == 'Frank' for user in users)

def test_add_duplicate_user_raises(test_app_context):
    """Test adding a duplicate user raises an error."""
    data_manager = SQLiteDataManager()
    data_manager.add_user('Frank')

    with pytest.raises(Exception):
        data_manager.add_user('Frank')


def test_delete_user(test_app_context):
    """Test deleting a user from the database."""
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.scalars(select(User)).all()
    assert any(user.name == 'TestUser1' for user in users)

    user_id = users[0].user_id
    data_manager.delete_user(user_id)

    users = db.session.scalars(select(User)).all()
    assert all('TestUser1' != user.name for user in users)


def test_delete_nonexistent_user_does_not_raise(test_app_context):
    """Test deleting a non-existent user does not raise an error."""
    data_manager = SQLiteDataManager()

    try:
        data_manager.delete_user(999)
    except Exception:
        pytest.fail("Deleting a non-existent user should not raise an error.")


def test_get_all_users(test_app_context):
    """Test retrieving all users."""
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    data_manager.add_user('TestUser2')

    users = data_manager.get_all_users()

    assert isinstance(users, list)
    assert len(users) >= 2
    assert any('TestUser1' == user.name for user in users)
    assert any('TestUser2' == user.name for user in users)


def test_add_movie(test_app_context):
    """Test adding a movie to a user's collection."""
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
    """Test retrieving all movies for a user."""
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
    """Test deleting a movie from a user's collection."""
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.scalars(select(User)).all()
    user_id = users[0].user_id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)
    data_manager.delete_movie(1, user_id)

    movies = db.session.scalars(select(Movie)).all()
    assert all('Titanic' != movie.title for movie in movies)


def test_delete_nonexistent_movie_does_not_raise(test_app_context):
    """Test that deleting a non-existent movie does not raise an exception."""
    data_manager = SQLiteDataManager()
    data_manager.add_user('TestUser')
    user_id = db.session.scalars(select(User)).first().user_id

    try:
        data_manager.delete_movie(movie_id=999, user_id=user_id)
    except Exception:
        pytest.fail("Deleting a non-existent movie should not raise an exception.")


def test_update_movie(test_app_context):
    """Test updating a movie's details."""
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser1')
    users = db.session.scalars(select(User)).all()
    user_id = users[0].user_id

    data_manager.add_movie(user_id, 'Titanic', 'Di Caprio', 1997, 9.9)

    update_movie = Movie(
        movie_id=1,
        title='Updated title',
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


def test_update_nonexistent_movie_raises_value_error(test_app_context):
    """Test that updating a non-existent movie raises a ValueError."""
    data_manager = SQLiteDataManager()

    non_existent_movie = Movie(
        movie_id=999,
        title='Ghost Movie',
        director='Nobody',
        year=1990,
        rating=5.0
    )

    with pytest.raises(ValueError, match="Movie not found."):
        data_manager.update_movie(non_existent_movie)


def test_update_movie_invalid_rating_raises(test_app_context):
    """Test updating a movie with invalid rating raises ValueError."""
    data_manager = SQLiteDataManager()

    data_manager.add_user('TestUser')
    user_id = db.session.scalars(select(User)).first().user_id
    data_manager.add_movie(user_id, 'Sample', 'Director', 2000, 5.0)

    movie = Movie(movie_id=1, title='Bad', director='Worse', year=2000, rating=100.0)

    with pytest.raises(ValueError):
        data_manager.update_movie(movie)


def test_update_movie_year_in_future_raises(test_app_context):
    """Test that updating a movie with a year in the future raises ValueError."""
    data_manager = SQLiteDataManager()
    data_manager.add_user('FutureTester')
    user_id = db.session.scalars(select(User)).first().user_id

    data_manager.add_movie(user_id, 'Time Machine', 'Director X', 2020, 5.5)

    future_year = datetime.now().year + 1
    movie = Movie(
        movie_id=1,
        title='Updated Title',
        director='Updated Director',
        year=future_year,
        rating=5.0
    )

    with pytest.raises(ValueError, match="Release year cannot be in the future."):
        data_manager.update_movie(movie)


def test_update_movie_year_too_old_raises(test_app_context):
    """Test that updating a movie with a year before 1888 raises ValueError."""
    data_manager = SQLiteDataManager()
    data_manager.add_user('PastTester')
    user_id = db.session.scalars(select(User)).first().user_id

    data_manager.add_movie(user_id, 'Oldie', 'Director Y', 1900, 6.0)

    movie = Movie(
        movie_id=1,
        title='Updated Oldie',
        director='Updated Director',
        year=1800,
        rating=6.0
    )

    with pytest.raises(ValueError, match="Release year cannot be older than 1888."):
        data_manager.update_movie(movie)


def test_get_movie_by_id(test_app_context):
    """Test retrieving a movie by its ID."""
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