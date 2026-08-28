"""Тесты для create_favicon tool."""

import pytest
from pathlib import Path
from PIL import Image

from mcp_server.tools.create_favicon import handler


@pytest.fixture
def test_png_icon(tmp_path: Path) -> Path:
    img = Image.new("RGBA", (512, 512), color=(255, 0, 0, 255))
    path = tmp_path / "icon.png"
    img.save(path, format="PNG")
    return path


@pytest.mark.asyncio
async def test_create_favicon_from_png(test_png_icon: Path) -> None:
    output_dir = test_png_icon.parent / "favicon"
    result = await handler({
        "source": str(test_png_icon.resolve()),
        "output_dir": str(output_dir),
    })
    assert result.isError is False or result.isError is None


@pytest.mark.asyncio
async def test_create_favicon_nonexistent() -> None:
    result = await handler({"source": "nonexistent.png"})
    assert result.isError is True
