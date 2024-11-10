import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_daily_breakdown(authenticated_async_client: AsyncClient):
    post = await authenticated_async_client.post(
        "http://test/api/posts/",
        json={
            "title": "Test1 title",
            "content": "Test1 content",
        }
    )

    post_id = post.json()["id"]

    comment_1 = await authenticated_async_client.post(
        "http://test/api/comments/",
        json={
            "content": "Test1 content comment",
            "post_id": post_id
        }
    )

    comment_2 = await authenticated_async_client.post(
        "http://test/api/comments/",
        json={
            "content": "Test2 content comment",
            "post_id": post_id
        }
    )

    today = datetime.date.today()

    date_to = today + datetime.timedelta(days=1)

    date_from = today.isoformat()
    date_to = date_to.isoformat()


    response = await authenticated_async_client.get(
        "http://test/api/comments-daily-breakdown",
        params={
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == 200
    assert response.json() == [
        {'comment_date': f'{date_from}', 'total_comments': 2, 'blocked_comments': 0}
    ]
