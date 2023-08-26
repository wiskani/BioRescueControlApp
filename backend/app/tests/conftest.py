from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine
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

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Drop all tables and create new ones
Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator [Session, None, None]:
    try:
        db: Session = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

def override_get_currrent_user() -> Users :
    email: EmailStr = EmailStr("dummy@dummy.com")
    user: Users = Users(id=5, email= email, name="dummy", last_name="dummy", permissions=["admin", ])
    return user

app.dependency_overrides[get_current_user]= override_get_currrent_user

client: TestClient = TestClient(app)
