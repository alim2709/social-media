from typing import List

from fastapi.params import Depends

from app.users.dependencies import AccessTokenBearer
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse


from app.social_media.schemas import SPostModel, SPostCreateModel, SPostUpdateModel
from app.social_media.service import SocialMediaService

social_media_router = APIRouter()
social_media_service = SocialMediaService()
access_token_bearer = AccessTokenBearer()

@social_media_router.get("/posts", response_model=List[SPostModel])
async def get_posts():
    posts = await social_media_service.get_posts()
    if not posts:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "There are no posts yet"})
    return posts


@social_media_router.get("/posts/{post_id}", response_model=SPostModel)
async def get_post_by_id(post_id):
    post = await social_media_service.get_post_by_id(post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


@social_media_router.post("/posts/", response_model=SPostModel)
async def create_post(post: SPostCreateModel, user_details = Depends(access_token_bearer)):
    post_data = post.model_dump()

    new_post = await social_media_service.create_post(author_id = int(user_details["user"]["id"]), **post_data)
    return SPostModel(
        id=new_post.id,
        title=new_post.title,
        content=new_post.content,
        created_at=new_post.created_at,
        is_blocked=new_post.is_blocked,
    )


@social_media_router.put("/posts/{post_id}", response_model=SPostModel)
async def update_post(post_id: int, new_data: SPostUpdateModel, user_details = Depends(access_token_bearer)):
    user_id = int(user_details["user"]["id"])
    new_data_dict = new_data.model_dump()
    new_post = await social_media_service.update_post(post_id, **new_data_dict)

    if not new_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if new_post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this post"
        )

    return SPostModel(
        id=new_post.id,
        title=new_post.title,
        content=new_post.content,
        created_at=new_post.created_at,
        is_blocked=new_post.is_blocked,
    )

@social_media_router.delete("/posts/{post_id}", response_model=SPostModel)
async def delete_post(post_id: int, user_details = Depends(access_token_bearer)):
    user_id = int(user_details["user"]["id"])

    post = await social_media_service.get_post_by_id(post_id)

    if post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this post"
        )

    await social_media_service.delete_post(post_id)

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "Post deleted"}
    )