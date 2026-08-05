"""Система логирования проекта MiMo Web Toolkit.

Предоставляет именованные логгеры для всех компонентов системы.
Использует стандартный модуль logging.
"""

import logging
from pathlib import Path


LOG_FORMAT = "%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logs_initialized = False
_logs_dir: Path | None = None


def setup_logging(
    level: int = logging.INFO,
    log_dir: Path | None = None,
) -> None:
    """Инициализирует систему логирования.

    Args:
        level: Уровень логирования (по умолчанию INFO).
        log_dir: Каталог для сохранения лог-файлов. Если None — только консоль.
    """
    global _logs_initialized, _logs_dir

    if _logs_initialized:
        return

    _logs_dir = log_dir

    root_logger = logging.getLogger("mcp_server")
    root_logger.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / "mcp_server.log",
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    _logs_initialized = True


def get_logger(name: str) -> logging.Logger:
    """Возвращает именованный логгер.

    Args:
        name: Имя логгера (обычно __name__ модуля).

    Returns:
        Экземпляр logging.Logger.
    """
    return logging.getLogger(f"mcp_server.{name}")
