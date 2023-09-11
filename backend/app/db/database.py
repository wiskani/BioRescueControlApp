from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.routers.config import get_settings, Settings

settings: Settings = get_settings()

DATABASE_URL = settings.DATABASE_URL


engine = create_async_engine(
                             DATABASE_URL,
                             echo=True,
                             )

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()
