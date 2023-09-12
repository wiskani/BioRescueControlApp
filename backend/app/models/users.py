from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from passlib.hash import bcrypt
from datetime import datetime

import app.db.database as _database

class User(_database.Base):
    __tablename__:str = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped [str] = mapped_column(String, index=True)
    permissions:Mapped[str] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    hashed_password: Mapped[str] = mapped_column(String)

    def verify_password(self, password:str)-> bool:
        return bcrypt.verify(password, self.hashed_password)

