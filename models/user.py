from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    movies = relationship("Movie", back_populates="user",
                          cascade="all, delete-orphan")
