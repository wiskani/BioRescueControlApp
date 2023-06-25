from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.users import UsersCreate,  Users, UsersResponse
from app.models.users import User
from app.crud.users import create_user, get_user_by_email
from app.api.deps import PermissonsChecker, get_db, get_current_user

router: APIRouter = APIRouter()

# Create new user
@router.post(
    path="/api/users",
    response_model=UsersResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Create a new user",
)
async def create_new_user(
    new_user: UsersCreate,
    db: Session = Depends(get_db),
    user: Users  = Depends(get_current_user) # Check if user is authenticated
) -> Users:
    db_user: User | None  = await get_user_by_email(db=db, email=new_user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        return await create_user(db = db, user = new_user)
