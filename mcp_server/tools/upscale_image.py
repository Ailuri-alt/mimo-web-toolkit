"""MCP-инструмент upscale_image.

Увеличение разрешения изображения.
Используется для масштабирования изображений с сохранением качества.
"""

from pathlib import Path
from typing import Any

from PIL import Image
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
            "description": "Путь к входному изображению",
        },
        "filename": {
            "type": "string",
            "description": "Имя итогового файла",
        },
        "scale": {
            "type": "integer",
            "description": "Множитель масштабирования",
            "minimum": 1,
            "maximum": 4,
            "default": 2,
        },
    },
    "required": ["image"],
}

DEFAULT_OUTPUT_DIR = Path("assets/optimized")


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента upscale_image.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        image = arguments.get("image", "")
        scale = arguments.get("scale", 2)
        filename = arguments.get("filename", "upscaled.webp")

        logger.info("upscale_image: image=%s, scale=%d, filename=%s", image, scale, filename)

        input_path = Path(image)
        if not input_path.exists():
            input_path = Path("assets/generated") / image

        if not input_path.exists():
            raise ImageProcessingError(f"Изображение не найдено: {image}")

        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = DEFAULT_OUTPUT_DIR / filename

        with Image.open(input_path) as img:
            new_width = img.width * scale
            new_height = img.height * scale
            upscaled = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            upscaled.save(output_path, format="WEBP", quality=85, method=6)

        logger.info("Изображение увеличено: %s -> %s (%dx)", input_path.name, output_path.name, scale)
        response = ImageResponse.success(file=output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageProcessingError as e:
        logger.error("upscale_image ошибка: %s", e)
        response = ImageResponse.failure("ImageProcessingError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("upscale_image непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
