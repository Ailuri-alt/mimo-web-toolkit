"""MCP-инструмент upscale_image.

Увеличение разрешения изображения методом LANCZOS-интерполяции.
Делегирует обработку в ImageProcessor.resize().
AI-upscaling не входит в v1.0.
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
        "scale": {
            "type": "integer",
            "description": "Множитель масштабирования (1-4)",
            "minimum": 1,
            "maximum": 4,
            "default": 2,
        },
    },
    "required": ["image"],
}


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

        processor = ImageProcessor()
        output_path = processor.resize(
            input_path=input_path,
            scale=scale,
            output_filename=filename,
        )

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
