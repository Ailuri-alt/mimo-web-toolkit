"""Провайдер для моделей FLUX.1 Schnell и FLUX.1 Dev.

Поддерживает:
- FLUX.1 Schnell (быстрая генерация);
- FLUX.1 Dev (максимальное качество);
- FLUX.1 Dev NF4 (оптимизация VRAM);
- FLUX GGUF (оптимизация VRAM).

Provider НЕ выполняет HTTP-запросы.
Для взаимодействия с ComfyUI используется ComfyClient.
"""

import json
from pathlib import Path
from typing import Any

from mcp_server.exceptions import ConfigurationError, WorkflowError
from mcp_server.logger import get_logger
from mcp_server.services.comfy.comfy_client import ComfyClient
from mcp_server.services.providers.base import ImageProvider

logger = get_logger(__name__)


class FluxProvider(ImageProvider):
    """Провайдер для моделей FLUX.1.

    Инкапсулирует особенности работы с FLUX моделями:
    - параметры генерации;
    - ограничения VRAM;
    - специфические настройки workflow.

    Attributes:
        comfy_client: ComfyClient для взаимодействия с ComfyUI.
        _model_name: Название модели.
        _vram_required: Требуемый объём VRAM в ГБ.
        _workflow_dir: Каталог с workflow.
    """

    def __init__(
        self,
        comfy_client: ComfyClient,
        model_name: str = "flux1-schnell",
        vram_required: int = 10,
        workflow_dir: Path | None = None,
    ) -> None:
        """Инициализирует FluxProvider.

        Args:
            comfy_client: ComfyClient для взаимодействия с ComfyUI.
            model_name: Название модели (по умолчанию flux1-schnell).
            vram_required: Требуемый объём VRAM в ГБ (по умолчанию 10).
            workflow_dir: Каталог с workflow (по умолчанию workflows/flux/).
        """
        self.comfy_client = comfy_client
        self._model_name = model_name
        self._vram_required = vram_required
        self._workflow_dir = workflow_dir or Path("workflows/flux")
        logger.info(
            "FluxProvider инициализирован: model=%s, vram=%dGB",
            model_name,
            vram_required,
        )

    @property
    def name(self) -> str:
        """Имя провайдера."""
        return f"flux-{self._model_name.replace('flux1-', '').replace('flux-', '')}"

    @property
    def model_name(self) -> str:
        """Название модели."""
        return self._model_name

    @property
    def vram_required(self) -> int:
        """Требуемый объём VRAM в ГБ."""
        return self._vram_required

    async def generate(
        self,
        prompt: str,
        workflow_path: Path,
        parameters: dict[str, Any] | None = None,
    ) -> Path:
        """Генерирует изображение через FLUX модель.

        Args:
            prompt: Промпт для генерации.
            workflow_path: Путь к JSON-workflow для ComfyUI.
            parameters: Дополнительные параметры генерации.

        Returns:
            Путь к сгенерированному изображению.

        Raises:
            WorkflowError: Если не удалось загрузить или выполнить workflow.
        """
        workflow = self._load_workflow(workflow_path)
        workflow = self._inject_prompt(workflow, prompt)

        if parameters:
            workflow = self._apply_parameters(workflow, parameters)

        logger.info("Отправка workflow в ComfyUI: %s", workflow_path.name)
        prompt_id = await self.comfy_client.queue_prompt(workflow)

        logger.info("Ожидание завершения: prompt_id=%s", prompt_id)
        result = await self.comfy_client.wait_for_completion(prompt_id)

        image_path = self._extract_image_path(result)
        logger.info("Изображение сгенерировано: %s", image_path)
        return image_path

    def validate(self) -> bool:
        """Проверяет, что провайдер готов к работе.

        Returns:
            True, если workflow-файлы доступны.
        """
        return self._workflow_dir.exists()

    def get_capabilities(self) -> dict[str, Any]:
        """Возвращает возможности провайдера.

        Returns:
            Словарь с информацией о возможностях модели.
        """
        return {
            "name": self.name,
            "model": self._model_name,
            "type": "diffusion",
            "vram_required": self._vram_required,
            "max_resolution": "2048x2048",
            "supports_lora": True,
        }

    def _load_workflow(self, workflow_path: Path) -> dict[str, Any]:
        """Загружает JSON-workflow.

        Args:
            workflow_path: Путь к файлу workflow.

        Returns:
            Словарь с workflow.

        Raises:
            WorkflowError: Если файл не найден или содержит ошибки.
        """
        if not workflow_path.exists():
            raise WorkflowError(f"Workflow не найден: {workflow_path}")

        try:
            with open(workflow_path, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise WorkflowError(f"Ошибка парсинга workflow: {e}") from e

    def _inject_prompt(self, workflow: dict[str, Any], prompt: str) -> dict[str, Any]:
        """Внедряет промпт в workflow.

        Args:
            workflow: Словарь с workflow.
            prompt: Промпт для генерации.

        Returns:
            Обновлённый workflow.
        """
        for node_id, node in workflow.items():
            if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
                inputs = node.get("inputs", {})
                if "text" in inputs:
                    inputs["text"] = prompt
                    logger.debug("Промпт внедрён в node %s", node_id)
        return workflow

    def _apply_parameters(
        self,
        workflow: dict[str, Any],
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """Применяет дополнительные параметры к workflow.

        Args:
            workflow: Словарь с workflow.
            parameters: Дополнительные параметры.

        Returns:
            Обновлённый workflow.
        """
        for node_id, node in workflow.items():
            if isinstance(node, dict) and node.get("class_type") == "KSampler":
                inputs = node.get("inputs", {})
                for key in ("sampler_name", "scheduler", "steps", "cfg", "seed"):
                    if key in parameters:
                        inputs[key] = parameters[key]
                        logger.debug("Параметр %s=%s применён к node %s", key, parameters[key], node_id)
        return workflow

    def _extract_image_path(self, result: dict[str, Any]) -> Path:
        """Извлекает путь к изображению из результата.

        Args:
            result: Результат генерации от ComfyUI.

        Returns:
            Путь к изображению.

        Raises:
            WorkflowError: Если изображение не найдено в результате.
        """
        outputs = result.get("outputs", {})

        for node_id, node_output in outputs.items():
            images = node_output.get("images", [])
            if images:
                image_info = images[0]
                filename = image_info.get("filename", "")
                subfolder = image_info.get("subfolder", "")
                return Path(subfolder) / filename if subfolder else Path(filename)

        raise WorkflowError("Изображение не найдено в результате генерации")
