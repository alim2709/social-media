from typing import Union

from fastapi import FastAPI
from app.users.routers import auth_router
from app.social_media.routers import social_media_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(social_media_router)
@app.get("/")
def read_root():
    return {"Hello": "World how are you"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}