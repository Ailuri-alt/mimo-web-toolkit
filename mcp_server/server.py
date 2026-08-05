"""MCP Server проекта MiMo Web Toolkit.

Точка входа MCP-сервера. Отвечает за:
- регистрацию MCP-инструментов;
- обработку запросов от MiMo Code;
- маршрутизацию запросов;
- возврат результатов.

MCP Server не содержит бизнес-логики генерации изображений.
Его задача — координация.
"""

from mcp_server.config_manager import ConfigManager
from mcp_server.logger import get_logger, setup_logging

logger = get_logger(__name__)


class MCPServer:
    """MCP Server для MiMo Web Toolkit.

    Координирует работу MCP-инструментов и обрабатывает запросы
    от AI-клиентов (MiMo Code, Claude Code и др.).

    Attributes:
        config: Менеджер конфигурации.
    """

    def __init__(self, config: ConfigManager | None = None) -> None:
        """Инициализирует MCP Server.

        Args:
            config: Менеджер конфигурации. Если None — создаётся новый.
        """
        self.config = config or ConfigManager()
        logger.info("MCPServer инициализирован")

    def start(self) -> None:
        """Запускает MCP Server.

        Загружает конфигурацию, регистрирует инструменты
        и начинает обработку входящих запросов.
        """
        logger.info("Запуск MCP Server...")
        self.config.load_settings()
        logger.info("Конфигурация загружена")
        logger.info("MCP Server готов к работе")

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
