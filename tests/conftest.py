import asyncio

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def test_app():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
