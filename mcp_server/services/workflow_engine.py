"""Workflow Engine — выбор и подготовка ComfyUI workflow.

Отвечает за:
- выбор подходящего workflow по purpose/style/aspect_ratio;
- загрузку JSON из workflows/flux/;
- предоставление параметров генерации.

Workflow Engine НЕ выполняет HTTP-запросы.
"""

import json
from pathlib import Path
from typing import Any

from mcp_server.config_manager import ConfigManager
from mcp_server.exceptions import ConfigurationError, WorkflowError
from mcp_server.logger import get_logger

logger = get_logger(__name__)


class WorkflowEngine:
    """Движок выбора workflow.

    Загружает конфигурацию workflow из config/workflows.yaml
    и предоставляет JSON-workflow для ComfyUI.

    Attributes:
        config: Менеджер конфигурации.
        workflow_dir: Каталог с JSON-workflow.
    """

    def __init__(
        self,
        config: ConfigManager | None = None,
        workflow_dir: Path | None = None,
    ) -> None:
        """Инициализирует Workflow Engine.

        Args:
            config: Менеджер конфигурации. Если None — создаётся новый.
            workflow_dir: Каталог с JSON-workflow. Если None — workflows/flux/.
        """
        self.config = config or ConfigManager()
        if not self.config.workflows:
            self.config.load_workflows()
        self.workflow_dir = workflow_dir or Path("workflows/flux")
        logger.info("WorkflowEngine инициализирован: %s", self.workflow_dir)

    def get_workflow_path(self, purpose: str) -> Path:
        """Возвращает путь к JSON-workflow для указанного purpose.

        Args:
            purpose: Тип изображения (hero, product, portrait и т.д.).

        Returns:
            Путь к JSON-workflow.

        Raises:
            ConfigurationError: Если конфигурация для purpose не найдена.
        """
        workflow_config = self.config.get_workflow_config(purpose)
        workflow_rel_path = workflow_config.get("workflow", "")

        if not workflow_rel_path:
            raise ConfigurationError(
                f"Путь к workflow не указан для: {purpose}"
            )

        return Path(workflow_rel_path)

    def load_workflow(self, purpose: str) -> dict[str, Any]:
        """Загружает JSON-workflow для указанного purpose.

        Args:
            purpose: Тип изображения.

        Returns:
            Словарь с workflow.

        Raises:
            WorkflowError: Если workflow не найден или содержит ошибки.
        """
        workflow_path = self.get_workflow_path(purpose)

        if not workflow_path.exists():
            raise WorkflowError(f"Workflow не найден: {workflow_path}")

        try:
            with open(workflow_path, encoding="utf-8") as f:
                workflow = json.load(f)
        except json.JSONDecodeError as e:
            raise WorkflowError(f"Ошибка парсинга workflow: {e}") from e

        logger.debug("Workflow загружен: %s", workflow_path)
        return workflow

    def get_generation_params(self, purpose: str) -> dict[str, Any]:
        """Возвращает параметры генерации для указанного purpose.

        Args:
            purpose: Тип изображения.

        Returns:
            Словарь с параметрами (sampler, scheduler, cfg, steps).

        Raises:
            ConfigurationError: Если конфигурация для purpose не найдена.
        """
        workflow_config = self.config.get_workflow_config(purpose)

        params = {}
        for key in ("sampler", "scheduler", "cfg", "steps"):
            if key in workflow_config:
                params[key] = workflow_config[key]

        logger.debug("Параметры генерации: purpose=%s, params=%s", purpose, params)
        return params

    def get_default_style(self, purpose: str) -> str:
        """Возвращает стиль по умолчанию для указанного purpose.

        Args:
            purpose: Тип изображения.

        Returns:
            Стиль по умолчанию.
        """
        workflow_config = self.config.get_workflow_config(purpose)
        return workflow_config.get("default_style", "photorealistic")

    def get_default_aspect_ratio(self, purpose: str) -> str:
        """Возвращает aspect ratio по умолчанию для указанного purpose.

        Args:
            purpose: Тип изображения.

        Returns:
            Aspect ratio по умолчанию.
        """
        workflow_config = self.config.get_workflow_config(purpose)
        return workflow_config.get("default_aspect_ratio", "16:9")

    def list_available_purposes(self) -> list[str]:
        """Возвращает список доступных purpose.

        Returns:
            Список purpose из конфигурации.
        """
        return list(self.config.workflows.keys())
