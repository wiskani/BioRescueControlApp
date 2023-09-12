import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator
from pydantic import EmailStr


from app.db.database import Base
from app.routers.config import get_settings, Settings
from app.api.deps import get_db, get_current_user
from app.schemas.users import Users
from app.main import app

settings: Settings = get_settings()


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_TEST

engine  = create_async_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Drop all tables and create new ones
async def drop_and_create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

loop = asyncio.get_event_loop()
loop.run_until_complete(drop_and_create_tables())


async def override_get_db() :
    try:
        db: AsyncSession = TestingSessionLocal()
        yield db
    finally:
        await db.close()


app.dependency_overrides[get_db] = override_get_db

def override_get_currrent_user() -> Users :
    email: EmailStr = "dummy@dummy.com"
    user: Users = Users(id=5, email= email, name="dummy", last_name="dummy", permissions=["admin", ])
    return user

app.dependency_overrides[get_current_user]= override_get_currrent_user

client: TestClient = TestClient(app)
