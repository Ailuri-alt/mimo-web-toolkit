"""Менеджер конфигурации проекта MiMo Web Toolkit.

Отвечает за загрузку, валидацию и предоставление настроек из YAML-файлов.
Все настройки проходят через этот модуль.
"""

from pathlib import Path
from typing import Any

import yaml

from mcp_server.exceptions import ConfigurationError
from mcp_server.logger import get_logger

logger = get_logger(__name__)

DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DEFAULT_SETTINGS_FILE = "settings.yaml"


class ConfigManager:
    """Менеджер конфигурации.

    Загружает YAML-файлы и предоставляет доступ к настройкам.
    Все компоненты системы получают настройки через этот класс.

    Attributes:
        config_dir: Путь к каталогу конфигурации.
        settings: Словарь с загруженными настройками.
    """

    def __init__(self, config_dir: Path | None = None) -> None:
        """Инициализирует менеджер конфигурации.

        Args:
            config_dir: Путь к каталогу конфигурации.
                        Если None — используется config/ в корне проекта.
        """
        self.config_dir = config_dir or DEFAULT_CONFIG_DIR
        self.settings: dict[str, Any] = {}
        logger.info("ConfigManager инициализирован: %s", self.config_dir)

    def load_settings(self, filename: str = DEFAULT_SETTINGS_FILE) -> dict[str, Any]:
        """Загружает файл настроек.

        Args:
            filename: Имя YAML-файла настроек.

        Returns:
            Словарь с загруженными настройками.

        Raises:
            ConfigurationError: Если файл не найден или содержит ошибки.
        """
        filepath = self.config_dir / filename

        if not filepath.exists():
            raise ConfigurationError(f"Файл конфигурации не найден: {filepath}")

        try:
            with open(filepath, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Ошибка парсинга YAML: {e}") from e

        if not isinstance(data, dict):
            raise ConfigurationError(
                f"Файл конфигурации должен содержать словарь: {filepath}"
            )

        self.settings = data
        logger.info("Конфигурация загружена: %s", filepath)
        return self.settings

    def get(self, key: str, default: Any = None) -> Any:
        """Возвращает значение настройки по ключу.

        Args:
            key: Ключ настройки (поддерживается точечная нотация: "comfyui.host").
            default: Значение по умолчанию, если ключ не найден.

        Returns:
            Значение настройки или default.
        """
        keys = key.split(".")
        value: Any = self.settings

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def get_section(self, section: str) -> dict[str, Any]:
        """Возвращает секцию настроек.

        Args:
            section: Имя секции (например, "comfyui").

        Returns:
            Словарь с настройками секции или пустой словарь.
        """
        value = self.settings.get(section, {})
        if isinstance(value, dict):
            return value
        return {}
