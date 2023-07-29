from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.routers.config import get_settings, Settings

settings: Settings = get_settings()

#DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = settings.DATABASE_URL


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
