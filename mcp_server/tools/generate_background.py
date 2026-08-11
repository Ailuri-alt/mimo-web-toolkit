"""MCP-инструмент generate_background.

Создание фоновых изображений.
Используется для генерации фонов для веб-сайтов и приложений.
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
        "subject": {
            "type": "string",
            "description": "Описание фона (например, abstract technology background)",
        },
        "filename": {
            "type": "string",
            "description": "Имя итогового файла",
        },
        "style": {
            "type": "string",
            "description": "Стиль фона",
            "enum": ["minimal", "gradient", "abstract", "photorealistic", "geometric"],
            "default": "minimal",
        },
        "aspect_ratio": {
            "type": "string",
            "description": "Соотношение сторон",
            "enum": ["16:9", "1:1", "4:3", "9:16"],
            "default": "16:9",
        },
    },
    "required": ["subject", "filename"],
}

PURPOSE = "background"


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента generate_background.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        subject = arguments.get("subject", "")
        style = arguments.get("style", "minimal")
        filename = arguments.get("filename", "background.webp")
        aspect_ratio = arguments.get("aspect_ratio", "16:9")

        logger.info(
            "generate_background: subject=%s, style=%s, filename=%s",
            subject,
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
            subject=subject,
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
        logger.info("generate_background завершён: %s", output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageGenerationError as e:
        logger.error("generate_background ошибка: %s", e)
        response = ImageResponse.failure("ImageGenerationError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("generate_background непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
