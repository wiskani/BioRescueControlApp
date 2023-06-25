import getpass

from functools import lru_cache
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr, ValidationError

from app.api.config import Settings
from app.db.database import engine, SessionLocal
from app.crud.users import get_first_user, create_user
from app.schemas.users import UsersCreate

import app.db.database as _database

#routes import
import app.routers.auth as  _auth
import app.routers.users as _users

_database.Base.metadata.create_all(bind=engine)


app:FastAPI = FastAPI()

#New decorator for cache
@lru_cache()
def get_settings():
    return Settings()

app.include_router(_auth.router)
app.include_router(_users.router)

#Route is used for import settings
@app.get("/api/settings")
async def settings(
    settings: Settings = Depends(get_settings)
) :
    return {
        "SECRET_KEY": settings.SECRET_KEY,
        "APP_MAX": settings.APP_MAX
    }



# Create first user
@app.on_event("startup")
async def startup() -> None:
    db: Session = SessionLocal()
    if await get_first_user(db) is None:
        id: int = 1
        while True:
            try:
                email_str: str = input("Enter email: ")
                email: EmailStr = EmailStr(email_str)
                break
            except ValidationError:
                print("El correo es invalido por favor coloque un correo valido")
        while True:
            password: str = getpass.getpass("Enter password: ")
            if 7 <= len(password) <= 30:
                break
            else:
                print("La contraseña debe tener al menos 8 caracteres y menos de 30")
        permissions: str = "admin"
        user: UsersCreate = UsersCreate(id=id, email=email, permissions=permissions, hashed_password=password)
        await create_user(db, user)
        print("User created")
