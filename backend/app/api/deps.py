import json
from pydantic import EmailStr
from typing import Union, AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, PyJWTError
from app.routers.config import get_settings, Settings
from app.db.database import get_db
from app.models.users import User
from app.schemas.users import Users, UsersAuth
from app.crud.users import get_user_by_email

oauth2scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/token")

settings: Settings = get_settings()
JWT_SECRET = settings.SECRET_KEY

if JWT_SECRET is None:
    raise ValueError("JWT_SECRET is not set")


# Create token
async def create_token(user: User) -> dict[str, str]:
    user_obj: UsersAuth = UsersAuth.from_orm(user)
    token: str = encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


# Get current user
async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2scheme)
        ) -> UsersAuth:

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="lost token"
        )
    try:
        payload: dict[str, str] = decode(
                token,
                JWT_SECRET,
                algorithms=["HS256"]
                )
        print(f"Decoded payload: {payload}")  # Logging the decoded payload

        result = await db.execute(select(User).filter_by(id=payload["id"]))
        user: User | None = result.scalars().first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        if not isinstance(user.permissions, list):
            user.permissions = json.loads(user.permissions)

    except PyJWTError as jwt_error:
        raise HTTPException(
            status_code=401,
            detail=f'Error in token decoding: {jwt_error}'
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f'Correo o password incorrecto: {e}'
        )

    return UsersAuth.from_orm(user)


# Authentication for login
async def authenticate_user(email: EmailStr, password: str, db: AsyncSession) -> User | bool:
    user: User | None = await get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


# Dependency for check permissions
class PermissonsChecker:
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: UsersAuth = Depends(get_current_user)) -> bool | HTTPException:
        for permission in self.required_permissions:
            if permission in user.permissions:
                return True
        raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos suficientes"
                )
