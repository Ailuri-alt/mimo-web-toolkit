"""Тесты для optimize_image tool."""

import pytest
from pathlib import Path

from mcp_server.tools.optimize_image import handler


@pytest.mark.asyncio
async def test_optimize_image_webp(test_image: Path) -> None:
    result = await handler({"image": str(test_image.resolve())})
    assert result.isError is False or result.isError is None


@pytest.mark.asyncio
async def test_optimize_image_png(test_image: Path) -> None:
    result = await handler({
        "image": str(test_image.resolve()),
        "format": "png",
    })
    assert result.isError is False or result.isError is None


@pytest.mark.asyncio
async def test_optimize_image_nonexistent() -> None:
    result = await handler({"image": "nonexistent.png"})
    assert result.isError is True


@pytest.mark.asyncio
async def test_optimize_image_with_quality(test_image: Path) -> None:
    result = await handler({
        "image": str(test_image.resolve()),
        "quality": 50,
    })
    assert result.isError is False or result.isError is None
