import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_post_create(authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.post(
        "http://test/api/posts/",
        json={
            "title": "Test title",
            "content": "Test content",
        }
    )

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_post_create_not_allowed(async_client: AsyncClient):
    response = await async_client.post(
        "http://test/api/posts/",
        json={
            "title": "Test title",
            "content": "Test content",
        }
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
async def test_get_posts(authenticated_async_client: AsyncClient):

    post_1 = await authenticated_async_client.post(
        "http://test/api/posts/",
        json={
            "title": "Test1 title",
            "content": "Test1 content",
        }
    )

    post_2 = await authenticated_async_client.post(
        "http://test/api/posts/",
        json={
            "title": "Test2 title",
            "content": "Test2 content",
        }
    )

    response = await authenticated_async_client.get(
        "http://test/api/posts/",
    )

    assert response.status_code == 200
    assert response.json() == [post_1.json(), post_2.json()]


@pytest.mark.asyncio
async def test_update_post(authenticated_async_client: AsyncClient):
    post_1 = await authenticated_async_client.post(
        "http://test/api/posts/",
        json={
            "title": "Test1 title",
            "content": "Test1 content",
        }
    )

    post_id = post_1.json().get("id")

    response = await authenticated_async_client.put(
        f"http://test/api/posts/{post_id}",
        json={
            "title": "Updated Test1 title",
            "content": "Updated Test1 content",
        },

    )
    assert response.status_code == 200

    updated_post = response.json()
    assert updated_post["id"] == post_id
    assert updated_post["title"] == "Updated Test1 title"
    assert updated_post["content"] == "Updated Test1 content"
    assert updated_post["created_at"] == post_1.json()["created_at"]
    assert updated_post["is_blocked"] == post_1.json()["is_blocked"]
    assert updated_post["author_id"] == post_1.json()["author_id"]


@pytest.mark.asyncio
async def test_delete_post(authenticated_async_client: AsyncClient):
    post_1 = await authenticated_async_client.post(
        "http://test/api/posts/",
        json={
            "title": "Test1 title",
            "content": "Test1 content",
        }
    )

    post_id = post_1.json().get("id")

    response = await authenticated_async_client.delete(
        f"http://test/api/posts/{post_id}",
    )

    assert response.status_code == 204
    assert response.json() == {"message": "Post deleted"}