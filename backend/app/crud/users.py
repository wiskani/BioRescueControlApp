from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from pydantic import EmailStr
from fastapi import HTTPException
from app.models.users import User
from app.schemas.users import UsersCreate

# Purpose: CRUD operations for users

#Get if user exists
async def get_first_user(db: Session) -> (User | None):
    return db.query(User).first()

# Get a user by email
async def get_user_by_email(db: Session, email: EmailStr) -> (User | None):
    return db.query(User).filter(User.email == email).first()

#Create a user
async def create_user(db: Session, user: UsersCreate) -> User:
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        return HTTPException(status_code=400, detail="Email already registered")
    else:
        db_user: User = User(email=user.email, permissions=user.permissions, hashed_password=bcrypt.hash(user.hashed_password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
 

