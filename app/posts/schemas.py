from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.comments.schemas import SCommentPostDetailModel


class SPostModel(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int

class SPostDetailModel(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int

    comments: list[SCommentPostDetailModel] = []

    model_config = ConfigDict(from_attributes=True)


class SPostCreateModel(BaseModel):
    title: str
    content: str

class SPostUpdateModel(BaseModel):
    title: str
    content: str

class SPostFilter(BaseModel):
    is_blocked: bool | None = None