from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from app.schemas.users import UsersCreate,  Users, UsersResponse
from app.models.users import User
from app.crud.users import create_user, get_user_by_email, update_user, delete_user, get_user_by_id
from app.api.deps import PermissonsChecker, get_db, get_current_user

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
    autorized: bool = Depends(PermissonsChecker(["admin"])), # Check if user is authorized
) -> Union[Users, HTTPException]:
    db_user: Union[User, None]  = await get_user_by_email(db=db, email=new_user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        return await create_user(db = db, user = new_user)

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
    autorized: bool = Depends(PermissonsChecker(["admin"])), # Check if user is authorized
) -> Union[Users, HTTPException]:
    db_user: Union[User, None] = await get_user_by_id(db=db, user_id=user_id)
    if db_user:
        return await update_user(db=db, user_id=user_id, user=user)
    else:
        raise HTTPException(status_code=400, detail="Something went wrong, maybe the user does not exist.")

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
    autorized: bool = Depends(PermissonsChecker(["admin"])), # Check if user is authorized
) -> Union[Users, HTTPException]:
    db_user: Union[User, None] = await get_user_by_id(db=db, user_id=user_id)
    if db_user:
        return await delete_user(db=db, user_id=user_id)
    else:
        raise HTTPException(status_code=400, detail="Something went wrong, maybe the user does not exist.")


