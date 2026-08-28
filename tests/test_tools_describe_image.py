"""Тесты для describe_image tool."""

import pytest
from pathlib import Path

from mcp_server.tools.describe_image import handler


@pytest.mark.asyncio
async def test_describe_image(test_image: Path) -> None:
    result = await handler({"image": str(test_image.resolve())})
    assert result.isError is False or result.isError is None


@pytest.mark.asyncio
async def test_describe_image_nonexistent() -> None:
    result = await handler({"image": "nonexistent.png"})
    assert result.isError is True


@pytest.mark.asyncio
async def test_describe_image_metadata(test_image: Path) -> None:
    result = await handler({"image": str(test_image.resolve())})
    content = result.content[0].text
    assert "success" in content
    assert "width" in content
    assert "height" in content
