import os
from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode

from app.db.database import SessionLocal
from app.models.users import User
from app.schemas.users import Users, UsersCreate
from app.crud.users import get_user_by_email

oauth2_scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = os.getenv("JWT_SECRET")

#Dependency
def get_db()-> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_token(user: User) -> dict[str, str]:
    user_obj:Users= Users.from_orm(user)

    token: str = encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

#Get current user
async def get_current_user(db: Session=Depends(get_db), token: str = Depends(oauth2_scheme)) -> Users:
    try:
        payload: dict[str, str] = decode(token, JWT_SECRET, algorithms=["HS256"])
        user  = db.query(User).get(payload["id"])
    except:
        raise HTTPException(
            status_code= 401,
            detail="Correo o password incorrecto"
        )
    return Users.from_orm(user)

#Authentication for login
async def authenticate_user(email: str, password: str, db: Session) -> (Users | bool):
    user:(User | None) = await get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


#Dependency for check permissions
class PermissonsChecker:
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: Users = Depends(get_current_user)) -> bool:
        for permission in self.required_permissions:
            if permission not in user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos suficientes"
                )
        return  True









