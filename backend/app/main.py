import getpass

from functools import lru_cache
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
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
import app.routers.species as _species
import app.routers.rescue_flora as _rescue_flora
import app.routers.images as _images

_database.Base.metadata.create_all(bind=engine)




app:FastAPI = FastAPI()

#Middleware for CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


#New decorator for cache
@lru_cache()
def get_settings():
    return Settings()

#Routes
app.include_router(_auth.router)
app.include_router(_users.router)
app.include_router(_species.router)
app.include_router(_rescue_flora.router)
app.include_router(_images.router)

#Route is used for import settings
@app.get("/api/settings")
async def _settings(
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
    settings: Settings  = get_settings()
    if await get_first_user(db) is None:
        id: int = 1
        while True:
            try:
                email_str: str = settings.FIRST_USER_MAIL
                email: EmailStr = EmailStr(email_str)
                break
            except ValidationError:
                print("email invalid")
        while True:
            password: str = settings.FIRST_USER_PASSWORD
            if 7 <= len(password) <= 30:
                break
            else:
                print("La contraseña debe tener al menos 8 caracteres y menos de 30")
        permissions: str = "admin"
        name: str = "admin"
        last_name: str = "admin"
        user: UsersCreate = UsersCreate(id=id, email=email, name=name, last_name=last_name, permissions=permissions, hashed_password=password)
        await create_user(db, user)
        print("User created")
