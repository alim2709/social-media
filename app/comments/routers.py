from typing import List

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.comments.schemas import SCommentModel
from app.comments.service import SocialMediaCommentService
from app.users.dependencies import AccessTokenBearer

comment_router = APIRouter()
comment_service = SocialMediaCommentService()
access_token_bearer = AccessTokenBearer()

@comment_router.get("/comments/", response_model=List[SCommentModel])
async def get_comments():
    comments = await comment_service.get_comments()
    if not comments:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "There are no comments yet"})
    return comments