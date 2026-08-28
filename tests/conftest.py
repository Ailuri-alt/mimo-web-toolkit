"""Общие fixtures для тестов."""

import pytest
from pathlib import Path
from PIL import Image


@pytest.fixture
def assets_dir() -> Path:
    """Каталог assets/test."""
    path = Path("assets/test")
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture
def test_image(assets_dir: Path) -> Path:
    """Создаёт тестовое изображение 100x100 PNG."""
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    path = assets_dir / "test_input.png"
    img.save(path, format="PNG")
    return path


@pytest.fixture
def test_image_webp(assets_dir: Path) -> Path:
    """Создаёт тестовое изображение 100x100 WebP."""
    img = Image.new("RGB", (100, 100), color=(0, 255, 0))
    path = assets_dir / "test_input.webp"
    img.save(path, format="WEBP", quality=85)
    return path
