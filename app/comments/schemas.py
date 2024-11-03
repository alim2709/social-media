from datetime import datetime

from pydantic import BaseModel

from app.models import Comment


class SCommentModel(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int
    post_id: int
    parent_id: int

    replies: list["Comment"]
