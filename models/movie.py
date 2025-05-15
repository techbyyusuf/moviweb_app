from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from main import db

class Movie(db.Model):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user = relationship('User', back_populates='movies')
    name: Mapped[str] = mapped_column(nullable=False, unique= True)
    year: Mapped[str] = mapped_column()
    director : Mapped[str] = mapped_column()
    rating : Mapped[float] = mapped_column()



