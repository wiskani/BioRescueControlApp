from fastapi import FastAPI

from app.db.database import engine

import app.db.database as _database

#routes import
import app.routers.auth as  _auth

_database.Base.metadata.create_all(bind=engine)


app:FastAPI = FastAPI()

app.include_router(_auth.router)
