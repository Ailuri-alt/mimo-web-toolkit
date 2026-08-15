"""MCP Server проекта MiMo Web Toolkit.

Точка входа MCP-сервера. Отвечает за:
- регистрацию MCP-инструментов;
- обработку запросов от MiMo Code;
- маршрутизацию запросов;
- возврат результатов.

MCP Server не содержит бизнес-логики генерации изображений.
Его задача — координация.
"""

import asyncio

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from mcp_server.config_manager import ConfigManager
from mcp_server.logger import get_logger, setup_logging
from mcp_server.registry import ToolRegistry
from mcp_server.tools.describe_image import handler as describe_image_handler
from mcp_server.tools.describe_image import INPUT_SCHEMA as describe_image_schema
from mcp_server.tools.generate_background import handler as generate_background_handler
from mcp_server.tools.generate_background import INPUT_SCHEMA as generate_background_schema
from mcp_server.tools.generate_icons import handler as generate_icons_handler
from mcp_server.tools.generate_icons import INPUT_SCHEMA as generate_icons_schema
from mcp_server.tools.generate_image import handler as generate_image_handler
from mcp_server.tools.generate_image import INPUT_SCHEMA as generate_image_schema
from mcp_server.tools.generate_logo import handler as generate_logo_handler
from mcp_server.tools.generate_logo import INPUT_SCHEMA as generate_logo_schema
from mcp_server.tools.generate_product_image import handler as generate_product_image_handler
from mcp_server.tools.generate_product_image import INPUT_SCHEMA as generate_product_image_schema
from mcp_server.tools.generate_team_photo import handler as generate_team_photo_handler
from mcp_server.tools.generate_team_photo import INPUT_SCHEMA as generate_team_photo_schema
from mcp_server.tools.optimize_image import handler as optimize_image_handler
from mcp_server.tools.optimize_image import INPUT_SCHEMA as optimize_image_schema
from mcp_server.tools.remove_background import handler as remove_background_handler
from mcp_server.tools.remove_background import INPUT_SCHEMA as remove_background_schema
from mcp_server.tools.upscale_image import handler as upscale_image_handler
from mcp_server.tools.upscale_image import INPUT_SCHEMA as upscale_image_schema

logger = get_logger(__name__)

APP_NAME = "mimo-web-toolkit"
APP_VERSION = "0.1.0"


class MCPServer:
    """MCP Server для MiMo Web Toolkit.

    Координирует работу MCP-инструментов и обрабатывает запросы
    от AI-клиентов (MiMo Code, Claude Code и др.).

    Attributes:
        config: Менеджер конфигурации.
        registry: Реестр MCP-инструментов.
        server: Экземпляр mcp.server.Server.
    """

    def __init__(self, config: ConfigManager | None = None) -> None:
        """Инициализирует MCP Server.

        Args:
            config: Менеджер конфигурации. Если None — создаётся новый.
        """
        self.config = config or ConfigManager()
        self.registry = ToolRegistry()
        self.server = Server(APP_NAME, version=APP_VERSION)
        self._register_tools()
        self._setup_handlers()
        logger.info("MCPServer инициализирован")

    def _register_tools(self) -> None:
        """Регистрирует MCP-инструменты."""
        self.registry.register(
            name="generate_image",
            description="Универсальная генерация изображений",
            input_schema=generate_image_schema,
            handler=generate_image_handler,
        )
        self.registry.register(
            name="generate_logo",
            description="Создание логотипов",
            input_schema=generate_logo_schema,
            handler=generate_logo_handler,
        )
        self.registry.register(
            name="generate_icons",
            description="Создание набора иконок",
            input_schema=generate_icons_schema,
            handler=generate_icons_handler,
        )
        self.registry.register(
            name="generate_background",
            description="Создание фоновых изображений",
            input_schema=generate_background_schema,
            handler=generate_background_handler,
        )
        self.registry.register(
            name="generate_team_photo",
            description="Создание изображений людей и команд",
            input_schema=generate_team_photo_schema,
            handler=generate_team_photo_handler,
        )
        self.registry.register(
            name="generate_product_image",
            description="Создание изображений товаров",
            input_schema=generate_product_image_schema,
            handler=generate_product_image_handler,
        )
        self.registry.register(
            name="remove_background",
            description="Конвертация и оптимизация изображения",
            input_schema=remove_background_schema,
            handler=remove_background_handler,
        )
        self.registry.register(
            name="optimize_image",
            description="Оптимизация изображений для веба",
            input_schema=optimize_image_schema,
            handler=optimize_image_handler,
        )
        self.registry.register(
            name="upscale_image",
            description="Увеличение разрешения изображения",
            input_schema=upscale_image_schema,
            handler=upscale_image_handler,
        )
        self.registry.register(
            name="describe_image",
            description="Анализ изображения",
            input_schema=describe_image_schema,
            handler=describe_image_handler,
        )
        logger.info("Инструменты зарегистрированы")

    def _setup_handlers(self) -> None:
        """Настраивает обработчики MCP-запросов."""
        registry = self.registry

        async def handle_list_tools(
            ctx: object, params: types.PaginatedRequestParams
        ) -> types.ListToolsResult:
            return types.ListToolsResult(tools=registry.list_tools())

        async def handle_call_tool(
            ctx: object, params: types.CallToolRequestParams
        ) -> types.CallToolResult:
            return await registry.call_tool(params.name, params.arguments or {})

        self.server.add_request_handler(
            "tools/list", types.PaginatedRequestParams, handle_list_tools
        )
        self.server.add_request_handler(
            "tools/call", types.CallToolRequestParams, handle_call_tool
        )
        logger.info("Обработчики MCP зарегистрированы")

    def start(self) -> None:
        """Запускает MCP Server.

        Загружает конфигурацию, регистрирует инструменты
        и начинает обработку входящих запросов через stdio.
        """
        logger.info("Запуск MCP Server...")
        self.config.load_all()
        logger.info("Конфигурация загружена: settings, prompts, workflows")
        logger.info("MCP Server готов к работе")
        asyncio.run(self._run())

    async def _run(self) -> None:
        """Запускает MCP Server в режиме stdio."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )

    def stop(self) -> None:
        """Останавливает MCP Server."""
        logger.info("Остановка MCP Server...")


def main() -> None:
    """Точка входа для запуска MCP Server через python -m mcp_server.server."""
    setup_logging()
    server = MCPServer()
    server.start()


if __name__ == "__main__":
    main()
