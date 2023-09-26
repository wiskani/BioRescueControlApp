import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import Generator
from pydantic import EmailStr


from app.db.database import Base
from app.routers.config import get_settings, Settings
from app.api.deps import get_db, get_current_user
from app.schemas.users import Users
from app.main import app

settings: Settings = get_settings()


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_TEST

engine  = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)
TestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
   loop = asyncio.get_event_loop_policy().new_event_loop()
   yield loop
   loop.close()

@pytest.fixture(scope="session")
async def init_test_db() :
    async with engine.begin() as conn:
        print("Iniciando base de datos de prueba...")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        print("Limpiando base de datos de prueba...")
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def override_get_db() :
    db: AsyncSession = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()



#app.dependency_overrides[get_db] = override_get_db

def override_get_current_user() -> Users :
    email: EmailStr = "dummy@dummy.com"
    user: Users = Users(id=5, email= email, name="dummy", last_name="dummy", permissions=["admin", ])
    return user

app.dependency_overrides[get_current_user]= override_get_current_user

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://localhost:8080") as ac:
        yield ac

