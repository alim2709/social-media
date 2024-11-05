from sqlalchemy import select, insert, update
from app.database import async_session_maker
from app.models import User


class UserService:
    def __init__(self, session=async_session_maker):
        self.session = session

    async def get_user_by_id(self, user_id):
        async with self.session() as session:
            query = select(User).where(User.id == user_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User:
        async with self.session() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def user_exists(self, email: str) -> bool:
        user = await self.get_user_by_email(email)

        return bool(user)

    async def create_user(self, **user_data) -> None:
        async with self.session() as session:
            query = insert(User).values(**user_data).returning(User)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def update_user(self, user_id: int, **user_data) -> None:
        async with self.session() as session:
            query = update(User).values(**user_data).where(User.id == user_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                return None

            updated_user = await self.get_user_by_id(user_id)
            return updated_user

