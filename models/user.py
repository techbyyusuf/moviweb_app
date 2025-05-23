from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.extensions import db


class User(db.Model):
    """Database model representing a user who owns movies."""

    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    movies = relationship(
        "Movie",
        back_populates="user",
        cascade="all, delete-orphan"
    )
