from typing import List

from fastapi import APIRouter, status, HTTPException, BackgroundTasks
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from app.comments.schemas import (
    SCommentModel,
    SCommentFilter,
    SCommentCreateModel,
    SCommentUpdateModel,
    SCommentDateFilter,
    SCommentDetailModel
)
from app.comments.service import SocialMediaCommentService
from app.posts.routers import post_service
from app.users.dependencies import AccessTokenBearer
from app.users.routers import user_service
from app.tasks import create_reply_for_comment
from app.utils import moderation_ai_posts_comments, get_automatic_reply_content

comment_router = APIRouter(prefix="/api")
comment_service = SocialMediaCommentService()
access_token_bearer = AccessTokenBearer()

@comment_router.get("/comments/", response_model=List[SCommentModel])
async def get_comments(filter_data: SCommentFilter = Depends()):

    comments = await comment_service.get_comments(filter_data)

    if not comments:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "There are no comments yet"})
    return comments


@comment_router.get("/comments/{comment_id}", response_model=SCommentDetailModel)
async def get_comment_by_id(comment_id):
    int_comment_id = int(comment_id)
    comment = await comment_service.get_comment_by_id(int_comment_id)
    if not comment or comment.is_blocked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found or blocked")
    return comment

@comment_router.post("/comments/", response_model=SCommentModel)
async def create_comment(
        background_tasks: BackgroundTasks,
        comment_data: SCommentCreateModel,
        user_details = Depends(access_token_bearer)
):
    comment_data_dict = comment_data.model_dump()
    author_id = int(user_details["user"]["id"])
    post = await post_service.get_post_by_id(post_id=int(comment_data_dict["post_id"]))

    if not post or post.is_blocked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or it is blocked")

    check_comment = moderation_ai_posts_comments(comment_data_dict["content"])

    if check_comment == "SAFETY":
        await comment_service.create_comment(author_id=author_id, is_blocked=True, **comment_data_dict)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Comment has been blocked for safety reasons")

    new_comment = await comment_service.create_comment(author_id = author_id, **comment_data_dict)

    author_of_post = await user_service.get_user_by_id(user_id=post.author_id)
    if author_of_post.auto_reply_enabled:
        text_reply_for_comment = get_automatic_reply_content(post_content=post.content, comment_content_to_reply=new_comment.content)
        background_tasks.add_task(
            create_reply_for_comment,
            text_reply_for_comment,
            new_comment.created_at,
            author_of_post.auto_reply_delay,
            author_of_post.id,
            post.id,
            new_comment.id,
        )

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


@comment_router.get("/comments-daily-breakdown")
async def get_daily_breakdown(filter_data: SCommentDateFilter = Depends()):

    result = await comment_service.get_comments_daily_breakdown(
        filter_data.date_from.isoformat(),
        filter_data.date_to.isoformat()
    )

    formatted_result = [
        {
            "comment_date": row.comment_date,
            "total_comments": row.total_comments,
            "blocked_comments": row.blocked_comments
        }
        for row in result
    ]

    if not formatted_result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No comments for this date"})
    return formatted_result
