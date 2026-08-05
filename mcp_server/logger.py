"""Система логирования проекта MiMo Web Toolkit.

Предоставляет именованные логгеры для всех компонентов системы.
Использует стандартный модуль logging с поддержкой уровней:
INFO, WARNING, ERROR, DEBUG.

Логи автоматически сохраняются в каталог logs/.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_FORMAT = "%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
MAX_LOG_SIZE_MB = 10
BACKUP_COUNT = 5

_logs_initialized = False
_logs_dir: Path | None = None


def setup_logging(
    level: int = logging.INFO,
    log_dir: Path | None = None,
) -> None:
    """Инициализирует систему логирования.

    Создаёт корневой логгер mcp_server с консольным и файловым обработчиками.
    Файловые логи автоматически ротируются при достижении MAX_LOG_SIZE_MB.

    Args:
        level: Уровень логирования. Поддерживаются:
               logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR.
               По умолчанию INFO.
        log_dir: Каталог для сохранения лог-файлов.
                 Если None — используется logs/ в корне проекта.
    """
    global _logs_initialized, _logs_dir

    if _logs_initialized:
        return

    _logs_dir = log_dir or DEFAULT_LOGS_DIR

    root_logger = logging.getLogger("mcp_server")
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    _logs_dir.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        _logs_dir / "mcp_server.log",
        maxBytes=MAX_LOG_SIZE_MB * 1024 * 1024,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    _logs_initialized = True


def get_logger(name: str) -> logging.Logger:
    """Возвращает именованный логгер.

    Логгер автоматически наследует обработчики от корневого логгера mcp_server.

    Args:
        name: Имя логгера (обычно __name__ модуля).

    Returns:
        Экземпляр logging.Logger с префиксом mcp_server.
    """
    return logging.getLogger(f"mcp_server.{name}")
