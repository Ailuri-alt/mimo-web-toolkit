"""MCP-инструмент optimize_image.

Оптимизация изображений для веба.
Делегирует обработку в ImageProcessor.process().
"""

from pathlib import Path
from typing import Any

from mcp import types

from mcp_server.exceptions import ImageProcessingError
from mcp_server.logger import get_logger
from mcp_server.models.image_response import ImageResponse
from mcp_server.services.image_processor import ImageProcessor

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
        "format": {
            "type": "string",
            "description": "Целевой формат (webp, png, jpg)",
            "enum": ["webp", "png", "jpg"],
            "default": "webp",
        },
        "quality": {
            "type": "integer",
            "description": "Качество (1-100)",
            "minimum": 1,
            "maximum": 100,
            "default": 85,
        },
    },
    "required": ["image"],
}


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента optimize_image.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        image = arguments.get("image", "")
        filename = arguments.get("filename", None)
        fmt = arguments.get("format", "webp")
        quality = arguments.get("quality", 85)

        logger.info(
            "optimize_image: image=%s, format=%s, quality=%d",
            image,
            fmt,
            quality,
        )

        input_path = Path(image)
        if not input_path.exists():
            input_path = Path("assets/generated") / image

        if not input_path.exists():
            raise ImageProcessingError(f"Изображение не найдено: {image}")

        processor = ImageProcessor()
        output_path = processor.process(
            input_path=input_path,
            output_filename=filename,
            output_format=fmt,
            quality=quality,
        )

        response = ImageResponse.success(file=output_path)
        logger.info("optimize_image завершён: %s", output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageProcessingError as e:
        logger.error("optimize_image ошибка: %s", e)
        response = ImageResponse.failure("ImageProcessingError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("optimize_image непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
