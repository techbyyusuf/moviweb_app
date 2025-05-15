from data_managers.data_manager_interface import DataManagerInterface
from app import db
from models.user import User
from models.movie import Movie
from sqlalchemy import select, update


class SQLiteDataManager(DataManagerInterface):

    def add_user(self, username: str):
        new_user = User(name=username)
        db.session.add(new_user)
        db.session.commit()


    def delete_user(self, user_id):
        user = db.session.get(User, user_id)
                                                                                # get user movies if >0 don't delete
        db.session.delete(user)
        db.session.commit()


    def get_all_users(self):
        stmt = select(User.name)
        return db.session.scalars(stmt).all()


    def add_movie(self, user_id, title, director, year, rating):
        new_movie = Movie(user_id=user_id,
                          name=title,
                          director=director,
                          year=year,
                          rating=rating)
        db.session.add(new_movie)
        db.session.commit()


    def get_user_movies(self, user_id):
        stmt = select(Movie).where(Movie.user_id == user_id)
        return db.session.scalars(stmt).all()


    def delete_movie(self, movie_id, user_id):
        movie = db.session.get(Movie, movie_id)

        db.session.delete(movie)

        #user_id = movie.user_id                                                #to check after website is created
        if len(self.get_user_movies(user_id)) == 0:
            self.delete_user(user_id)

        db.session.commit()


    def update_movie(self, movie):
        db_movie = db.session.get(Movie, movie.movie_id)
        if db_movie:
            db_movie.name = movie.name
            db_movie.director = movie.director
            db_movie.year = movie.year
            db_movie.rating = movie.rating

            db.session.commit()