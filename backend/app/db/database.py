from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.routers.config import get_settings, Settings

settings: Settings = get_settings()

DATABASE_URL = settings.DATABASE_URL


#Engine
engine = create_async_engine(
                             DATABASE_URL,
                             echo=True,
                             )

#Session
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,

)

#Base
class Base(DeclarativeBase):
    pass

#Create tables
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#Dependency
async def get_db():
    async with SessionLocal.begin() as db:
        try:
            yield db
        except:
            await db.rollback()
            raise
        finally:
            await db.close()


