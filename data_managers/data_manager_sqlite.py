from flask_sqlalchemy import SQLAlchemy
from data_managers.data_manager_interface import DataManagerInterface
from main import db
from models.user import User
from models.movie import Movie
from sqlalchemy import select


class SQLiteDataManager(DataManagerInterface):

    def add_user(self, username: str):
        new_user = User(name=username)
        db.session.add(new_user)
        db.session.commit()

    def delete_user(self, user_id):
        user = db.session.get(User, user_id)
        db.session.delete(user)
        db.session.commit()

    def get_all_users(self):
        stmt = select(User.name)
        return db.session.scalars(stmt).all()

    def add_user_movie(self, user_id, title, director, year, rating):
        # users = data_manager.SQLiteDataManager
        # if any(f{user_id} for user in users)
        new_movie = Movie(user_id=user_id,
                          name=title,
                          director=director,
                          year=year,
                          rating=rating)
        db.session.add(new_movie)
        db.session.commit()

    def delete_user_movie(self, user_id, id):
        pass

    def get_user_movies(self, user_id):
        pass

    def update_user_movie(self, user_id, title, director, year, rating):
        pass