from sqlalchemy import select, insert, update, delete

from app.database import async_session_maker
from app.models import Comment


class SocialMediaCommentService:
    session = async_session_maker()

    async def get_comments(self):
        async with self.session as session:
            query = select(Comment)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_post_comments(self, post_id):
        async with self.session as session:
            query = select(Comment).where(Comment.post_id == post_id)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_author_comments(self, author_id):
        async with self.session as session:
            query = select(Comment).where(Comment.author_id == author_id)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_comment_by_id(self, comment_id):
        async with self.session as session:
            query = select(Comment).where(Comment.id == comment_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()


    async def create_comment(self, **comment_data):
        async with self.session as session:
            query = insert(Comment).values(**comment_data).returning(Comment)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def update_comment(self, comment_id, **comment_data):
        async with self.session as session:
            query = update(Comment).values(**comment_data).where(Comment.id == comment_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                return None

            updated_comment = await self.get_comment_by_id(comment_id)
            return updated_comment

    async def delete_comment(self, comment_id):
        async with self.session as session:
            query = delete(Comment).where(Comment.id == comment_id)
            await session.execute(query)
            await session.commit()