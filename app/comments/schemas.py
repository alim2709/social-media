from datetime import datetime
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
