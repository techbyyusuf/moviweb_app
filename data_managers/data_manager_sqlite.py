from models.user import User
from models.movie import Movie
from utils.extensions import db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from data_managers.data_manager_interface import DataManagerInterface
from datetime import datetime


class SQLiteDataManager(DataManagerInterface):

    def add_user(self, name):
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding user: {e}")
            raise



    def delete_user(self, user_id):
        try:
            user = db.session.get(User, user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting user: {e}")
            raise


    def get_all_users(self):
        try:
            return db.session.scalars(select(User)).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving users: {e}")
            return []


    def add_movie(self, user_id, title, director, year, rating):
        try:
            new_movie = Movie(
                user_id=user_id,
                title=title,
                director=director,
                year=year,
                rating=rating
            )
            db.session.add(new_movie)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding movie: {e}")
            raise


    def get_user_movies(self, user_id):
        try:
            stmt = select(Movie).where(Movie.user_id == user_id)
            return db.session.scalars(stmt).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving user movies: {e}")
            return []


    def delete_movie(self, movie_id, user_id):
        try:
            stmt = select(Movie).where(Movie.movie_id == movie_id, Movie.user_id == user_id)
            movie = db.session.scalars(stmt).first()
            if movie:
                db.session.delete(movie)
                db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting movie: {e}")
            raise


    def update_movie(self, movie):
        try:
            if int(movie.year) > datetime.now().year:
                raise ValueError("Release year cannot be in the future.")
            if 0 < float(movie.rating) < 10.0:
                raise ValueError("Rating must be between 0 and 10.")

            db_movie = db.session.get(Movie, movie.movie_id)
            if db_movie:
                db_movie.title = movie.title
                db_movie.director = movie.director
                db_movie.year = movie.year
                db_movie.rating = movie.rating
                db.session.commit()
        except (SQLAlchemyError, ValueError) as e:
            db.session.rollback()
            print(f"Error updating movie: {e}")
            raise


    def get_movie_by_id(self, movie_id):
        try:
            stmt = select(Movie).where(Movie.movie_id == movie_id)
            return db.session.scalars(stmt).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving movie by ID: {e}")
            return None