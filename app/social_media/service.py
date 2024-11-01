from sqlalchemy import select, insert, update, delete

from app.database import async_session_maker
from app.models import Post


class SocialMediaService:
    session = async_session_maker()

    async def get_posts(self):
        async with self.session as session:
            query = select(Post)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_post_by_id(self, post_id):
        async with self.session as session:
            query = select(Post).where(Post.id == post_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    async def create_post(self, **post_data):
        async with self.session as session:
            query = insert(Post).values(**post_data).returning(Post)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def update_post(self, post_id, **post_data):
        async with self.session as session:
            query = update(Post).values(**post_data).where(Post.id == post_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                return None

            updated_post = await self.get_post_by_id(post_id)
            return updated_post

    async def delete_post(self, post_id):
        async with self.session as session:
            query = delete(Post).where(Post.id == post_id)
            result = await session.execute(query)
            await session.commit()

