import json
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Union
from passlib.hash import bcrypt
from pydantic import EmailStr
from fastapi import HTTPException
from app.models.users import User
from app.schemas.users import UsersCreate, Users

# Purpose: CRUD operations for users


# Get if user exists
async def get_first_user(db: AsyncSession) -> User | None:
    result = await db.execute(select(User).limit(1))
    return result.scalars().first()


# Get all users
async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return list(result.scalars().all())


# Get a user by email
async def get_user_by_email(db: AsyncSession, email: EmailStr) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    db_user = result.scalars().first()

    if db_user:
        try:
            db_user.permissions = json.loads(db_user.permissions)
            return db_user
        except Exception as e:
            print("Error parsing permissions", e)
        return db_user
    return None


# Get a user by id
async def get_user_by_id(
        db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


# Create a user
async def create_user(
        db: AsyncSession,
        user: UsersCreate
        ) -> User | HTTPException:
    db_user = await get_user_by_email(db, user.email)
    if db_user is not None:
        return HTTPException(
                status_code=400,
                detail="Email already registered"
                )
    else:
        db_user = User(
            email=user.email,
            name=user.name,
            last_name=user.last_name,
            permissions=user.permissions,
            hashed_password=bcrypt.hash(user.hashed_password)
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user


# Update a user by id
async def update_user(
        db: AsyncSession,
        user_id: int,
        user: Users
        ) -> User:
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        db_user.email = user.email
        db_user.name = user.name
        db_user.last_name = user.last_name
        db_user.permissions = user.permissions
        db_user.hashed_password = bcrypt.hash(user.hashed_password)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=400, detail="User does not exist")


# Delete a user by id
async def delete_user(
        db: AsyncSession,
        user_id: int
        ) -> dict | HTTPException:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return HTTPException(status_code=400, detail="User does not exist")
    else:
        await db.execute(delete(User).where(User.id == user_id))
        await db.commit()
        return {"message": "User deleted"}
