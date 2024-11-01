from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
from contextlib import asynccontextmanager


DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_= AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

class Base(DeclarativeBase):
    pass