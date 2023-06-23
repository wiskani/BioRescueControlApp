import getpass

from fastapi import FastAPI
from sqlalchemy.orm import Session
from pydantic import EmailStr, ValidationError

from app.db.database import engine, SessionLocal
from app.crud.users import get_first_user, create_user
from app.schemas.users import UsersCreate

import app.db.database as _database

#routes import
import app.routers.auth as  _auth

_database.Base.metadata.create_all(bind=engine)


app:FastAPI = FastAPI()

app.include_router(_auth.router)

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
        user: UsersCreate = UsersCreate(id=id, email=email, permissions=permissions, password=password)
        await create_user(db, user)
        print("User created")
