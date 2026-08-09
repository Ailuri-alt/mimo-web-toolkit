"""Prompt Engine — система шаблонов промптов.

Превращает высокоуровневые параметры (purpose, subject, style)
в полноценные профессиональные промпты.

Prompt Engine не содержит информации о workflow.
"""

from typing import Any

from mcp_server.config_manager import ConfigManager
from mcp_server.exceptions import PromptError
from mcp_server.logger import get_logger

logger = get_logger(__name__)


class PromptEngine:
    """Движок формирования промптов.

    Загружает шаблоны из config/prompts.yaml и формирует
    промпты на основе purpose, subject и style.

    Prompt Engine НЕ содержит информации о workflow.

    Attributes:
        config: Менеджер конфигурации.
    """

    def __init__(self, config: ConfigManager | None = None) -> None:
        """Инициализирует Prompt Engine.

        Args:
            config: Менеджер конфигурации. Если None — создаётся новый.
        """
        self.config = config or ConfigManager()
        if not self.config.prompts:
            self.config.load_prompts()
        logger.info("PromptEngine инициализирован")

    def build_prompt(
        self,
        purpose: str,
        subject: str,
        style: str = "photorealistic",
        aspect_ratio: str = "16:9",
        **kwargs: Any,
    ) -> str:
        """Формирует промпт на основе параметров.

        Args:
            purpose: Тип изображения (hero, product, portrait и т.д.).
            subject: Описание объекта изображения.
            style: Стиль изображения.
            aspect_ratio: Соотношение сторон.
            **kwargs: Дополнительные переменные для шаблона.

        Returns:
            Сформированный промпт.

        Raises:
            PromptError: Если шаблон для purpose не найден.
        """
        template_data = self.config.get_prompt_template(purpose)
        template = template_data.get("template", "")

        if not template:
            raise PromptError(f"Шаблон промпта пуст для: {purpose}")

        variables = {
            "subject": subject,
            "style": style,
            "aspect_ratio": aspect_ratio,
            **kwargs,
        }

        try:
            prompt = template.format(**variables)
        except KeyError as e:
            raise PromptError(
                f"Отсутствует переменная {e} в шаблоне для: {purpose}"
            ) from e

        logger.debug("Промпт сформирован: purpose=%s, длина=%d", purpose, len(prompt))
        return prompt.strip()

    def get_negative_prompt(self, purpose: str) -> str:
        """Возвращает negative prompt для указанного типа изображения.

        Args:
            purpose: Тип изображения.

        Returns:
            Negative prompt или пустая строка.
        """
        template_data = self.config.get_prompt_template(purpose)
        negative = template_data.get("negative", "")
        return negative.strip() if negative else ""
