"""MCP-инструмент generate_image.

Универсальный инструмент генерации изображений.
Используется, когда MiMo требуется создать изображение общего назначения.
"""

from pathlib import Path
from typing import Any

from mcp import types

from mcp_server.config_manager import ConfigManager
from mcp_server.exceptions import ImageGenerationError
from mcp_server.logger import get_logger
from mcp_server.models.image_request import ImageRequest
from mcp_server.models.image_response import ImageResponse
from mcp_server.services.comfy.comfy_client import ComfyClient
from mcp_server.services.prompt_engine import PromptEngine
from mcp_server.services.providers.flux_provider import FluxProvider
from mcp_server.services.workflow_engine import WorkflowEngine

logger = get_logger(__name__)

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "purpose": {
            "type": "string",
            "description": "Тип изображения",
            "enum": ["hero", "background", "illustration", "product", "portrait", "custom"],
        },
        "subject": {
            "type": "string",
            "description": "Описание объекта изображения",
        },
        "filename": {
            "type": "string",
            "description": "Имя итогового файла",
        },
        "style": {
            "type": "string",
            "description": "Стиль изображения",
            "enum": ["photorealistic", "cinematic", "minimal", "3d", "illustration"],
        },
        "aspect_ratio": {
            "type": "string",
            "description": "Соотношение сторон",
            "enum": ["16:9", "1:1", "4:3", "9:16"],
        },
    },
    "required": ["purpose", "subject", "filename"],
}


async def handler(arguments: dict[str, Any]) -> types.CallToolResult:
    """Обработчик MCP-инструмента generate_image.

    Args:
        arguments: Входные параметры инструмента.

    Returns:
        Результат выполнения инструмента.
    """
    try:
        request = ImageRequest.from_dict(arguments)
        logger.info(
            "generate_image: purpose=%s, subject=%s, filename=%s",
            request.purpose,
            request.subject,
            request.filename,
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
            purpose=request.purpose,
            subject=request.subject,
            style=request.style,
            aspect_ratio=request.aspect_ratio,
        )
        workflow_path = workflow_engine.get_workflow_path(request.purpose)

        output_path = Path("assets/generated") / request.filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        await provider.generate(
            prompt=prompt,
            workflow_path=workflow_path,
            parameters=request.parameters,
        )

        response = ImageResponse.success(file=output_path)
        logger.info("generate_image завершён: %s", output_path)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))]
        )

    except ImageGenerationError as e:
        logger.error("generate_image ошибка: %s", e)
        response = ImageResponse.failure("ImageGenerationError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
    except Exception as e:
        logger.error("generate_image непредвиденная ошибка: %s", e)
        response = ImageResponse.failure("UnexpectedError", str(e))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=str(response.to_dict()))],
            isError=True,
        )
