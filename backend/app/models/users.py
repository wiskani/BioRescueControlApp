from sqlalchemy import Column, Integer, String
from passlib.hash import bcrypt

import app.db.database as _database

class User(_database.Base):
    __tablename__:str = "users"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    email: Column[str] = Column(String, unique=True, index=True)
    permissions:Column[str] = Column(String)
    hashed_password: Column[str] = Column(String)

    def verify_password(self, password:str)-> bool:
        return bcrypt.verify(password, self.hashed_password)

