from flask_sqlalchemy import SQLAlchemy
from data_managers.data_manager_interface import DataManagerInterface
from main import db
from models.user import User
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
        user_names = db.session.execute(stmt)
        return [row[0] for row in user_names]

    def get_user_movies(self, user_id):
        pass

    def delete_user_movie(self, user_id, id):
        pass

    def add_user_movie(self, user_id, title, director, year, rating):
        pass


    def update_user_movie(self, user_id, title, director, year, rating):
        pass