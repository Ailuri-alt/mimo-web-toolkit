"""MCP-инструмент describe_image.

Анализ изображения.
Используется для создания alt, title и описаний изображений.
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
            "description": "Путь к изображению для анализа",
        },
    },
    "required": ["image"],
}


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента describe_image.

    Анализирует изображение и возвращает:
    - формат;
    - размеры;
    - цветовой режим;
    - размер файла.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        image = arguments.get("image", "")

        logger.info("describe_image: image=%s", image)

        input_path = Path(image)
        if not input_path.exists():
            input_path = Path("assets/generated") / image

        if not input_path.exists():
            raise ImageProcessingError(f"Изображение не найдено: {image}")

        processor = ImageProcessor()
        info = processor.get_info(input_path)

        response = ImageResponse.success(
            file=input_path,
            metadata={
                "format": info.get("format"),
                "mode": info.get("mode"),
                "width": info.get("width"),
                "height": info.get("height"),
                "size_bytes": info.get("size_bytes"),
                "alt_text": f"Image: {input_path.stem}",
                "title": f"{input_path.stem}",
            },
        )

        logger.info("describe_image завершён: %s", input_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageProcessingError as e:
        logger.error("describe_image ошибка: %s", e)
        response = ImageResponse.failure("ImageProcessingError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("describe_image непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
