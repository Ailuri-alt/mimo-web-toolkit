"""Тесты для remove_background tool."""

import pytest
from pathlib import Path

from mcp_server.tools.remove_background import handler


@pytest.mark.asyncio
async def test_remove_background(test_image: Path) -> None:
    result = await handler({"image": str(test_image.resolve())})
    assert result.isError is False or result.isError is None


@pytest.mark.asyncio
async def test_remove_background_nonexistent() -> None:
    result = await handler({"image": "nonexistent.png"})
    assert result.isError is True
