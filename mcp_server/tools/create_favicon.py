"""MCP-инструмент create_favicon.

Создание favicon.ico и apple-touch-icon.png из SVG/PNG.

Использует cairosvg (для SVG→PNG) + Pillow (для resize и ICO).
"""

from pathlib import Path
from typing import Any

from mcp import types

from mcp_server.exceptions import ImageProcessingError
from mcp_server.logger import get_logger
from mcp_server.models.image_response import ImageResponse

logger = get_logger(__name__)

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "source": {
            "type": "string",
            "description": "Путь к исходному изображению (SVG или PNG)",
        },
        "output_dir": {
            "type": "string",
            "description": "Каталог для сохранения favicon (по умолчанию assets/favicon)",
        },
    },
    "required": ["source"],
}

DEFAULT_OUTPUT_DIR = Path("assets/favicon")

FAVICON_SIZES = [(16, 16), (32, 32), (48, 48)]
APPLE_TOUCH_ICON_SIZE = (180, 180)


def _load_as_pil(source_path: Path) -> Any:
    """Загружает изображение как PIL Image.

    Для SVG конвертирует через cairosvg, для PNG/PIL использует Pillow напрямую.

    Args:
        source_path: Путь к изображению.

    Returns:
        PIL.Image.Image
    """
    from PIL import Image
    import io

    if source_path.suffix.lower() == ".svg":
        try:
            import cairosvg
        except ImportError:
            raise ImageProcessingError(
                "cairosvg не установлен. Установите: pip install cairosvg"
            )

        png_data = cairosvg.svg2png(url=str(source_path))
        return Image.open(io.BytesIO(png_data))

    return Image.open(source_path)


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента create_favicon.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        from PIL import Image as PILImage

        source = arguments.get("source", "")
        output_dir = arguments.get("output_dir", str(DEFAULT_OUTPUT_DIR))

        logger.info("create_favicon: source=%s, output_dir=%s", source, output_dir)

        source_path = Path(source)
        if not source_path.exists():
            source_path = Path("assets/generated") / source

        if not source_path.exists():
            raise ImageProcessingError(f"Исходное изображение не найдено: {source}")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        img = _load_as_pil(source_path)

        if img.mode in ("RGBA", "P"):
            base_img = img.convert("RGBA")
        else:
            base_img = img.convert("RGB")

        favicon_path = output_path / "favicon.ico"
        base_img.save(
            favicon_path,
            format="ICO",
            sizes=FAVICON_SIZES,
        )
        logger.info("favicon.ico создан: %s", favicon_path)

        apple_icon = base_img.copy()
        apple_icon.thumbnail(APPLE_TOUCH_ICON_SIZE, PILImage.Resampling.LANCZOS)
        apple_icon_path = output_path / "apple-touch-icon.png"
        apple_icon.save(apple_icon_path, format="PNG")
        logger.info("apple-touch-icon.png создан: %s", apple_icon_path)

        response = ImageResponse.success(
            file=favicon_path,
            metadata={
                "favicon_ico": str(favicon_path),
                "apple_touch_icon": str(apple_icon_path),
                "sizes": [f"{s[0]}x{s[1]}" for s in FAVICON_SIZES],
            },
        )
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageProcessingError as e:
        logger.error("create_favicon ошибка: %s", e)
        response = ImageResponse.failure("ImageProcessingError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("create_favicon непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
