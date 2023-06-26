from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from pydantic import EmailStr
from fastapi import HTTPException
from app.models.users import User
from app.schemas.users import UsersCreate, Users

# Purpose: CRUD operations for users

#Get if user exists
async def get_first_user(db: Session) -> (User | None):
    return db.query(User).first()

# Get a user by email
async def get_user_by_email(db: Session, email: EmailStr) -> (User | None):
    return db.query(User).filter(User.email == email).first()

# Get a user by id
async def get_user_by_id(db: Session, user_id: int) -> (User | None):
    return db.query(User).filter(User.id == user_id).first()

#Create a user
async def create_user(db: Session, user: UsersCreate) -> (User | HTTPException):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        return HTTPException(status_code=400, detail="Email already registered")
    else:
        db_user: User = User(email=user.email, permissions=user.permissions, hashed_password=bcrypt.hash(user.hashed_password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

#Update a user by id
async def update_user(db: Session, user_id: int, user: Users) -> (User | HTTPException):
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        db_user.email = user.email
        db_user.permissions = user.permissions
        db_user.hashed_password = bcrypt.hash(user.hashed_password)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return HTTPException(status_code=400, detail="User does not exist")

#Delete a user by id
async def delete_user(db: Session, user_id: int) -> (User | HTTPException):
    try:
        db_user = await get_user_by_id(db, user_id)
        db.delete(db_user)
        db.commit()
        return db_user
    except:
        return HTTPException(status_code=400, detail="User does not exist")




 

