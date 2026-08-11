"""MCP-инструмент remove_background.

Удаление фона изображения.
Используется для создания изображений с прозрачным фоном.
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
    },
    "required": ["image"],
}


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента remove_background.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        image = arguments.get("image", "")
        filename = arguments.get("filename", "no_background.webp")

        logger.info("remove_background: image=%s, filename=%s", image, filename)

        input_path = Path(image)
        if not input_path.exists():
            input_path = Path("assets/generated") / image

        if not input_path.exists():
            raise ImageProcessingError(f"Изображение не найдено: {image}")

        processor = ImageProcessor()
        output_path = processor.process(
            input_path,
            output_filename=filename,
            output_format="webp",
        )

        response = ImageResponse.success(file=output_path)
        logger.info("remove_background завершён: %s", output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageProcessingError as e:
        logger.error("remove_background ошибка: %s", e)
        response = ImageResponse.failure("ImageProcessingError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("remove_background непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
