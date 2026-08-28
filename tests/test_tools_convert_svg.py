"""Тесты для convert_svg tool."""

import pytest
from pathlib import Path

from mcp_server.tools.convert_svg import handler


@pytest.mark.asyncio
async def test_convert_svg_nonexistent() -> None:
    result = await handler({"image": "nonexistent.svg"})
    assert result.isError is True


@pytest.mark.asyncio
async def test_convert_svg_not_svg(tmp_path: Path) -> None:
    png_file = tmp_path / "test.png"
    png_file.write_bytes(b"not an svg")
    result = await handler({"image": str(png_file)})
    assert result.isError is True
