"""MCP-инструмент generate_icons.

Создание набора иконок.
Используется для генерации иконок с определённой тематикой и стилем.
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
        "theme": {
            "type": "string",
            "description": "Тематика иконок",
            "enum": ["medical", "technology", "business", "education", "food", "travel"],
        },
        "count": {
            "type": "integer",
            "description": "Количество иконок",
            "minimum": 1,
            "maximum": 50,
            "default": 12,
        },
        "style": {
            "type": "string",
            "description": "Стиль иконок",
            "enum": ["outline", "filled", "duotone", "flat"],
            "default": "outline",
        },
        "filename": {
            "type": "string",
            "description": "Имя итогового файла",
        },
    },
    "required": ["theme", "filename"],
}

PURPOSE = "icons"


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента generate_icons.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        theme = arguments.get("theme", "business")
        count = arguments.get("count", 12)
        style = arguments.get("style", "outline")
        filename = arguments.get("filename", "icons.webp")

        logger.info(
            "generate_icons: theme=%s, count=%d, style=%s, filename=%s",
            theme,
            count,
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
            subject=theme,
            style=style,
            count=count,
            theme=theme,
        )
        workflow_path = workflow_engine.get_workflow_path(PURPOSE)

        output_path = Path("assets/generated") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        await provider.generate(
            prompt=prompt,
            workflow_path=workflow_path,
        )

        response = ImageResponse.success(file=output_path)
        logger.info("generate_icons завершён: %s", output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageGenerationError as e:
        logger.error("generate_icons ошибка: %s", e)
        response = ImageResponse.failure("ImageGenerationError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("generate_icons непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
