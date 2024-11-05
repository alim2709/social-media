from datetime import datetime

from pydantic import BaseModel


class SPostModel(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    is_blocked: bool
    author_id: int


class SPostCreateModel(BaseModel):
    title: str
    content: str

class SPostUpdateModel(BaseModel):
    title: str
    content: str

class SPostFilter(BaseModel):
    is_blocked: bool | None = None