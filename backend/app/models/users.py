from sqlalchemy import Column, Integer, String, DateTime, JSON
from passlib.hash import bcrypt
from datetime import datetime

import app.db.database as _database

class User(_database.Base):
    __tablename__:str = "users"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    email: Column[str] = Column(String, unique=True, index=True)
    name: Column[str] = Column(String, index=True)
    last_name: Column [str] = Column(String, index=True)
    permissions:Column[str] = Column(JSON)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())
    hashed_password: Column[str] = Column(String)

    def verify_password(self, password:str)-> bool:
        return bcrypt.verify(password, self.hashed_password)

