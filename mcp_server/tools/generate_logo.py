"""MCP-инструмент generate_logo.

Создание логотипов.
Используется, когда сайт требует логотип компании, знак бренда или favicon.
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
        "brand_name": {
            "type": "string",
            "description": "Название бренда или компании",
        },
        "style": {
            "type": "string",
            "description": "Стиль логотипа",
            "enum": ["minimal", "modern", "classic", "playful", "corporate"],
            "default": "minimal",
        },
        "filename": {
            "type": "string",
            "description": "Имя итогового файла",
        },
        "aspect_ratio": {
            "type": "string",
            "description": "Соотношение сторон",
            "enum": ["1:1", "16:9", "4:3"],
            "default": "1:1",
        },
    },
    "required": ["brand_name", "filename"],
}

PURPOSE = "logo"


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента generate_logo.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        brand_name = arguments.get("brand_name", "")
        style = arguments.get("style", "minimal")
        filename = arguments.get("filename", "logo.webp")
        aspect_ratio = arguments.get("aspect_ratio", "1:1")

        logger.info(
            "generate_logo: brand_name=%s, style=%s, filename=%s",
            brand_name,
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
            subject=brand_name,
            style=style,
            aspect_ratio=aspect_ratio,
        )
        workflow_path = workflow_engine.get_workflow_path(PURPOSE)

        output_path = Path("assets/generated") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        await provider.generate(
            prompt=prompt,
            workflow_path=workflow_path,
        )

        response = ImageResponse.success(file=output_path)
        logger.info("generate_logo завершён: %s", output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageGenerationError as e:
        logger.error("generate_logo ошибка: %s", e)
        response = ImageResponse.failure("ImageGenerationError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("generate_logo непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
