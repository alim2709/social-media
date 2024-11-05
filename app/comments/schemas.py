from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class SCommentModel(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int
    post_id: int
    parent_id: Optional[int]

class SCommentPostDetailModel(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int

    model_config = ConfigDict(from_attributes=True)

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
    is_blocked: bool | None = None

class SCommentDateFilter(BaseModel):
    date_from: date
    date_to: date


class SCommentDetailModel(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int
    post_id: int
    parent_id: Optional[int]
    replies: List["SCommentModel"] = []


    model_config = ConfigDict(from_attributes=True)

SCommentDetailModel.model_rebuild()