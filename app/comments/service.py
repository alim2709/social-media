from datetime import datetime

from sqlalchemy import select, insert, update, delete, cast, Date, func, case

from app.database import async_session_maker
from app.models import Comment


class SocialMediaCommentService:
    session = async_session_maker()

    async def get_comments(self, filter_data = None):
        async with self.session as session:
            query = select(Comment)
            if filter_data:
                if filter_data.author_id:
                    query = query.where(Comment.author_id == filter_data.author_id)
                if filter_data.post_id:
                    query = query.where(Comment.post_id == filter_data.post_id)

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

    async def get_comments_daily_breakdown(self, date_from: str, date_to: str):
        date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")

        async with self.session as session:
            query = (
                select(
                cast(Comment.created_at, Date).label("comment_date"),
                func.count().label("total_comments"),
                func.sum(case(
                    (Comment.is_blocked == True, 1),
                    else_=0)).label("blocked_comments")
            )
                .where(Comment.created_at.between(date_from_dt, date_to_dt))
                .group_by(cast(Comment.created_at, Date))
                .order_by("comment_date")
            )

            result = await session.execute(query)
            return result.fetchall()
