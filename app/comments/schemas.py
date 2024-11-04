from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class SCommentModel(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int
    post_id: int
    parent_id: Optional[int]


class SCommentCreateModel(BaseModel):
    content: str
    post_id: int


class SCommentUpdateModel(BaseModel):
    content: str


class SCommentReplyCreateModel(BaseModel):
    content: str
    post_id: int
    parent_id: int


class SCommentReplyUpdateModel(SCommentReplyCreateModel):
    pass


class SCommentFilter(BaseModel):
    author_id: int | None = None
    post_id: int | None = None

class SCommentDateFilter(BaseModel):
    date_from: date
    date_to: date
