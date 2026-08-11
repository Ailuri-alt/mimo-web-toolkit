"""MCP-инструмент generate_product_image.

Создание изображений товаров.
Используется для генерации карточек товаров и коммерческих фото.
"""

from pathlib import Path
from typing import Any

from mcp import types

from mcp_server.config_manager import ConfigManager
from mcp_server.exceptions import ImageGenerationError
from mcp_server.logger import get_logger
from mcp_server.models.image_response import ImageResponse
from mcp_server.services.comfy.comfy_client import ComfyClient
from mcp_server.services.prompt_engine import PromptEngine
from mcp_server.services.providers.flux_provider import FluxProvider
from mcp_server.services.workflow_engine import WorkflowEngine

logger = get_logger(__name__)

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "product": {
            "type": "string",
            "description": "Название или описание товара",
        },
        "filename": {
            "type": "string",
            "description": "Имя итогового файла",
        },
        "style": {
            "type": "string",
            "description": "Стиль фото",
            "enum": ["studio photography", "lifestyle", "minimal", "luxury"],
            "default": "studio photography",
        },
        "background": {
            "type": "string",
            "description": "Фон изображения",
            "enum": ["white", "gray", "black", "gradient", "transparent"],
            "default": "white",
        },
        "aspect_ratio": {
            "type": "string",
            "description": "Соотношение сторон",
            "enum": ["1:1", "16:9", "4:3"],
            "default": "1:1",
        },
    },
    "required": ["product", "filename"],
}

PURPOSE = "product"


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента generate_product_image.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        product = arguments.get("product", "")
        style = arguments.get("style", "studio photography")
        background = arguments.get("background", "white")
        filename = arguments.get("filename", "product.webp")
        aspect_ratio = arguments.get("aspect_ratio", "1:1")

        logger.info(
            "generate_product_image: product=%s, style=%s, filename=%s",
            product,
            style,
            filename,
        )

        config = ConfigManager()
        config.load_all()

        prompt_engine = PromptEngine(config)
        workflow_engine = WorkflowEngine(config)

        comfy_client = ComfyClient(
            host=config.get("comfyui.host", "127.0.0.1"),
            port=config.get("comfyui.port", 8188),
            timeout=config.get("comfyui.timeout", 600),
        )

        provider = FluxProvider(
            comfy_client=comfy_client,
            model_name="flux1-schnell",
            vram_required=10,
        )

        prompt = prompt_engine.build_prompt(
            purpose=PURPOSE,
            subject=product,
            style=style,
            aspect_ratio=aspect_ratio,
            background=background,
        )
        workflow_path = workflow_engine.get_workflow_path(PURPOSE)

        output_path = Path("assets/generated") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        await provider.generate(
            prompt=prompt,
            workflow_path=workflow_path,
        )

        response = ImageResponse.success(file=output_path)
        logger.info("generate_product_image завершён: %s", output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageGenerationError as e:
        logger.error("generate_product_image ошибка: %s", e)
        response = ImageResponse.failure("ImageGenerationError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("generate_product_image непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
