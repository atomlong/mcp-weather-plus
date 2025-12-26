import pytest
import respx
import pytest_asyncio
from typing import AsyncGenerator

@pytest_asyncio.fixture
async def respx_mock() -> AsyncGenerator[respx.MockRouter, None]:
    async with respx.mock(base_url="https://") as respx_mock:
        yield respx_mock
