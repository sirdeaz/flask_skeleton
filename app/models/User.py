from flask_login import UserMixin
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f'<User {self.first_name} {self.last_name}>'

