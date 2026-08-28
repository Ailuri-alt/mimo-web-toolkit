"""Тесты для upscale_image tool."""

import pytest
from pathlib import Path

from mcp_server.tools.upscale_image import handler


@pytest.mark.asyncio
async def test_upscale_image_2x(test_image: Path) -> None:
    result = await handler({"image": str(test_image.resolve()), "scale": 2})
    assert result.isError is False or result.isError is None


@pytest.mark.asyncio
async def test_upscale_image_nonexistent() -> None:
    result = await handler({"image": "nonexistent.png"})
    assert result.isError is True


@pytest.mark.asyncio
async def test_upscale_image_default_scale(test_image: Path) -> None:
    result = await handler({"image": str(test_image.resolve())})
    assert result.isError is False or result.isError is None
