from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.extensions import db


class Movie(db.Model):
    """Database model for a movie associated with a user."""

    __tablename__ = 'movies'
    __table_args__ = (db.UniqueConstraint('title', 'user_id'),)

    movie_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    user = relationship('User', back_populates='movies')
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    year: Mapped[int] = mapped_column()
    director: Mapped[str] = mapped_column()
    rating: Mapped[float] = mapped_column()
