from typing import Union

from fastapi import FastAPI
from app.users.routers import auth_router
from app.posts.routers import post_router
from app.comments.routers import comment_router

app = FastAPI(
    title="Social Media API",
    summary="API for managing users, posts and comments"
)

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}