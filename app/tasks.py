import asyncio
from datetime import datetime, timedelta
from app.comments.service import SocialMediaCommentService


comment_service = SocialMediaCommentService()

async def create_reply_for_comment(
        text_reply_for_comment: str,
        comment_created_at: datetime,
        delay_to_create_reply_in_minutes: int,
        author_reply_id: int,
        post_id: int,
        parent_comment_id: int,

):
    delay_in_seconds = delay_to_create_reply_in_minutes * 60
    await asyncio.sleep(delay_in_seconds)
    await comment_service.create_comment(
        content=text_reply_for_comment,
        created_at=comment_created_at + timedelta(seconds=delay_in_seconds),
        author_id=author_reply_id,
        post_id=post_id,
        parent_id=parent_comment_id,
    )
