"""MCP-инструмент convert_svg.

Конвертация SVG-изображений в растровые форматы.
Делегирует в cairosvg + Pillow.

Поддерживаемые направления:
- SVG → PNG
- SVG → WebP

v1.0: PNG → SVG не реализуется (требует vectorization).
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
        "image": {
            "type": "string",
            "description": "Путь к входному SVG-файлу",
        },
        "filename": {
            "type": "string",
            "description": "Имя итогового файла",
        },
        "format": {
            "type": "string",
            "description": "Целевой формат (png, webp)",
            "enum": ["png", "webp"],
            "default": "png",
        },
    },
    "required": ["image"],
}

DEFAULT_OUTPUT_DIR = Path("assets/optimized")


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента convert_svg.

    Конвертирует SVG в PNG или WebP через cairosvg + Pillow.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        image = arguments.get("image", "")
        filename = arguments.get("filename", None)
        fmt = arguments.get("format", "png")

        logger.info("convert_svg: image=%s, format=%s", image, fmt)

        input_path = Path(image)
        if not input_path.exists():
            input_path = Path("assets/generated") / image

        if not input_path.exists():
            raise ImageProcessingError(f"Изображение не найдено: {image}")

        if input_path.suffix.lower() != ".svg":
            raise ImageProcessingError(
                f"Входной файл должен быть SVG: {input_path.suffix}"
            )

        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        if filename is None:
            filename = f"{input_path.stem}.{fmt}"

        output_path = DEFAULT_OUTPUT_DIR / filename

        try:
            import cairosvg
            from PIL import Image
            import io

            png_data = cairosvg.svg2png(url=str(input_path))

            if fmt == "png":
                output_path.write_bytes(png_data)
            elif fmt == "webp":
                img = Image.open(io.BytesIO(png_data))
                img.save(output_path, format="WEBP", quality=85, method=6)
            else:
                raise ImageProcessingError(
                    f"Неподдерживаемый формат: {fmt}. Допустимые: png, webp"
                )

        except ImportError:
            raise ImageProcessingError(
                "cairosvg не установлен. Установите: pip install cairosvg"
            )

        response = ImageResponse.success(file=output_path)
        logger.info("convert_svg завершён: %s -> %s", input_path.name, output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageProcessingError as e:
        logger.error("convert_svg ошибка: %s", e)
        response = ImageResponse.failure("ImageProcessingError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("convert_svg непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
