from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from pydantic import EmailStr

from app.schemas.users import UsersCreate,  Users, UsersResponse
from app.models.users import User
from app.crud.users import (
        create_user,
        get_all_users,
        get_user_by_email,
        update_user,
        delete_user,
        get_user_by_id
        )
from app.api.deps import PermissonsChecker, get_db

router: APIRouter = APIRouter()


# Create new user
@router.post(
    path="/api/users",
    response_model=UsersResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Create a new user",
)
async def create_new_user(
    new_user: UsersCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[Users, HTTPException]:
    db_user: Union[User, None] = await get_user_by_email(
            db=db,
            email=new_user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        return await create_user(db=db, user=new_user)


# Get all users
@router.get(
    path="/api/users",
    response_model=list[UsersResponse],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get all users",
)
async def get_users(
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> list[UsersResponse]:
    users = await get_all_users(db=db)
    users_db = []
    for user in users:
        users_db.append(UsersResponse(
            id=user.id,
            email=user.email,
            permissions=user.permissions,
            name=user.name,
            last_name=user.last_name
            ))
    return users_db


# Get user by id
@router.get(
    path="/api/users/{user_id}",
    response_model=UsersResponse,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Get a user by id",
)
async def get_user_by_id_api(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> Union[UsersResponse, HTTPException]:
    db_user: Union[User, None] = await get_user_by_id(db=db, user_id=user_id)
    if db_user:
        return UsersResponse(
            id=db_user.id,
            email=db_user.email,
            permissions=db_user.permissions,
            name=db_user.name,
            last_name=db_user.last_name
            )
    else:
        raise HTTPException(
                status_code=400,
                detail="Something went wrong, maybe the user does not exist."
                )


# Update user by id
@router.put(
    path="/api/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=None,
    tags=["Users"],
    summary="Update a user by id",
)
async def update_user_by_id(
    user_id: int,
    user: UsersCreate,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"]))
) -> UsersResponse | HTTPException:
    db_user: Union[User, None] = await get_user_by_id(db=db, user_id=user_id)
    if db_user:
        db_user_update = await update_user(db=db, user_id=user_id, user=user)
        if db_user_update:
            return UsersResponse(
                id=db_user_update.id,
                email=db_user_update.email,
                permissions=db_user_update.permissions,
                name=db_user_update.name,
                last_name=db_user_update.last_name
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Something went wrong, maybe the user does not exist."
                )
    else:
        raise HTTPException(
                status_code=400,
                detail="Something went wrong, maybe the user does not exist."
                )


# Delete user by id
@router.delete(
    path="/api/users/{user_id}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    summary="Delete a user by id",
)
async def delete_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    autorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Union[Users, HTTPException]:
    db_user: Union[User, None] = await get_user_by_id(db=db, user_id=user_id)
    if db_user:
        return await delete_user(db=db, user_id=user_id)
    else:
        raise HTTPException(
                status_code=400,
                detail="Something went wrong, maybe the user does not exist."
                )
