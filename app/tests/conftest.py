import pytest
from sqlalchemy import text

from app.database import Base, async_session_maker, engine
from app.config import settings

from httpx import AsyncClient, ASGITransport
from app.main import app as fastapi_app



@pytest.fixture(scope="session", autouse=True)
async def prepare_database():

    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def async_client ():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app)) as ac:
        yield ac

@pytest.fixture(scope="function")
async def authenticated_async_client(async_client):
    async with AsyncClient(transport=ASGITransport(app=fastapi_app)) as ac:
        await ac.post(
            "http://test/api/signup",
            json={
                "username": "test_auth",
                "email": "test_auth@test.com",
                "password": "test_auth_user"
            }
        )

        login_response = await ac.post(
            "http://test/api/login",
            json={
                "email": "test_auth@test.com",
                "password": "test_auth_user"
            }
        )

        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            if token:
                ac.headers.update({"Authorization": f"Bearer {token}"})
            else:
                raise ValueError("No access_token found in login response.")
        else:
            raise ValueError(f"Login failed with status {login_response.status_code}")

        yield ac

@pytest.fixture(scope="function", autouse=True)
async def clear_data():
    async with async_session_maker() as session:
        await session.execute(text("TRUNCATE TABLE users, posts, comments RESTART IDENTITY CASCADE;"))
        await session.commit()

    yield

    async with async_session_maker() as session:
        await session.execute(text("TRUNCATE TABLE users, posts, comments RESTART IDENTITY CASCADE;"))
        await session.commit()
