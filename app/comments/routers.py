from typing import List

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.comments.schemas import SCommentModel, SCommentFilter, SCommentCreateModel, SCommentUpdateModel
from app.comments.service import SocialMediaCommentService
from app.posts.routers import post_service
from app.users.dependencies import AccessTokenBearer

comment_router = APIRouter()
comment_service = SocialMediaCommentService()
access_token_bearer = AccessTokenBearer()

@comment_router.get("/comments/", response_model=List[SCommentModel])
async def get_comments(filter_data: SCommentFilter = Depends()):

    comments = await comment_service.get_comments(filter_data)
    if not comments:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "There are no comments yet"})
    return comments

@comment_router.post("/comments/", response_model=SCommentModel)
async def create_comment(comment_data: SCommentCreateModel, user_details = Depends(access_token_bearer)):
    comment_data_dict = comment_data.model_dump()
    author_id = int(user_details["user"]["id"])
    post = await post_service.get_post_by_id(post_id=int(comment_data_dict["post_id"]))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    new_comment = await comment_service.create_comment(author_id = author_id, **comment_data_dict)

    return new_comment
@comment_router.put("/comments/{comment_id}", response_model=SCommentModel)
async def update_comment(
        comment_id: int,
        comment_data: SCommentUpdateModel,
        user_details = Depends(access_token_bearer)
):
    user_id = int(user_details["user"]["id"])
    comment_data_dict = comment_data.model_dump()
    updated_comment = await comment_service.update_comment(comment_id = comment_id, **comment_data_dict)

    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if updated_comment.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this comment"
        )

    return updated_comment


@comment_router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, user_details = Depends(access_token_bearer)):
    user_id = int(user_details["user"]["id"])

    comment = await comment_service.get_comment_by_id(comment_id)

    if comment.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this comment"
        )

    await comment_service.delete_comment(comment_id)

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "Comment deleted"}
    )
