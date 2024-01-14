from functools import lru_cache
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from pydantic import EmailStr, ValidationError

from app.api.config import Settings
from app.db.database import engine, SessionLocal, init_tables
from app.crud.users import get_first_user, create_user
from app.schemas.users import UsersCreate
from app.middlewares.error_handler import ErrorHandler

import app.db.database as _database

#routes import
import app.routers.auth as  _auth
import app.routers.users as _users
import app.routers.species as _species
import app.routers.rescue_flora as _rescue_flora
import app.routers.images as _images
import app.routers.files as _files
import app.routers.tower as _tower
import app.routers.services.api_gdif as _api_gdif
import app.routers.rescue_herpetofauna as _rescue_herpetofauna
import app.routers.rescue_mammals as _rescue_mamals
import app.routers.services.nivo as _nivo

app:FastAPI = FastAPI()
app.title = "Rescue Bio API"
app.version = "0.0.1"

# make a static files path
app.mount("/static", StaticFiles(directory="/fastapi/static") , name="static")

#Middleware for error handler
app.add_middleware(ErrorHandler)



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

#Middleware for CORS
origins = [
    "http://localhost:3000",
    get_settings().NEXTJS_URL,
]
#Routes
app.include_router(_auth.router)
app.include_router(_users.router)
app.include_router(_species.router)
app.include_router(_rescue_flora.router)
app.include_router(_images.router)
app.include_router(_files.router)
app.include_router(_tower.router)
app.include_router(_api_gdif.router)
app.include_router(_rescue_herpetofauna.router)
app.include_router(_rescue_mamals.router)
app.include_router(_nivo.router)

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
    #comment this line if you want to create a new database and tables with alembic
    #await init_tables()

    db = SessionLocal()
    settings: Settings  = get_settings()
    if await get_first_user(db) is None:
        id: int = 1
        while True:
            try:
                email:EmailStr| str = settings.FIRST_USER_MAIL
                break
            except ValidationError:
                print("email invalid")
        while True:
            password: str = settings.FIRST_USER_PASSWORD
            if 7 <= len(password) <= 30:
                break
            else:
                print("La contraseña debe tener al menos 8 caracteres y menos de 30")
        permissions: List[str] = ["admin", ]
        name: str = "admin"
        last_name: str = "admin"
        user: UsersCreate = UsersCreate(id=id, email=email, name=name, last_name=last_name, permissions=permissions, hashed_password=password)
        await create_user(db, user)
    await db.close()
