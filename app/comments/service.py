from datetime import datetime

from sqlalchemy import select, insert, update, delete, cast, Date, func, case, or_
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
from app.models import Comment


class SocialMediaCommentService:
    def __init__(self, session=async_session_maker):
        self.session = session

    async def get_comments(self, filter_data = None):
        async with self.session() as session:
            query = select(Comment)
            if filter_data:
                if filter_data.author_id:
                    query = query.where(Comment.author_id == filter_data.author_id)
                if filter_data.post_id:
                    query = query.where(Comment.post_id == filter_data.post_id)
                if filter_data.is_blocked is not None:
                    query = query.where(Comment.is_blocked == filter_data.is_blocked)

            result = await session.execute(query)
            result_full = result.scalars().all()

            return result_full


    async def get_comment_by_id(self, comment_id):
        async with self.session() as session:

            query = (
                select(Comment)
                .options(joinedload(Comment.replies))
                .where(or_(Comment.id == comment_id,Comment.parent_id == comment_id))
                .order_by(Comment.created_at)
            )
            result = await session.execute(query)
            comments = result.unique().scalars().all()

            comment_dict = {comment.id: comment for comment in comments}

            root_comment = comment_dict.get(comment_id)
            if not root_comment:
                return None

            for comment in comments:
                if comment.parent_id:
                    parent_comment = comment_dict.get(comment.parent_id)
                    if parent_comment and comment not in parent_comment.replies:
                        parent_comment.replies.append(comment)

            return root_comment


    async def create_comment(self, **comment_data):
        async with self.session() as session:
            query = insert(Comment).values(**comment_data).returning(Comment)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def update_comment(self, comment_id, **comment_data):
        async with self.session() as session:
            query = update(Comment).values(**comment_data).where(Comment.id == comment_id)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                return None

            updated_comment = await self.get_comment_by_id(comment_id)
            return updated_comment

    async def delete_comment(self, comment_id):
        async with self.session() as session:
            query = delete(Comment).where(Comment.id == comment_id)
            await session.execute(query)
            await session.commit()

    async def get_comments_daily_breakdown(self, date_from: str, date_to: str):
        date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")

        async with self.session() as session:
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
