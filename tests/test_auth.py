import pytest
from httpx import AsyncClient
from app.main import app
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.user import Base

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(settings.database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(engine):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post("/auth/register", json={
        "email": "admin@example.com",
        "password": "string12345",
        "full_name": "firstadmin"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@example.com"

@pytest.mark.asyncio
async def test_login(client):
    # First register
    await client.post("/auth/register", json={
        "email": "test2@example.com",
        "password": "password",
        "full_name": "Test User"
    })
    response = await client.post("/auth/login", data={
        "username": "test2@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"