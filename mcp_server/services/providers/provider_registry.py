"""Реестр провайдеров моделей.

Управляет регистрацией и выбором провайдеров генерации изображений.
"""

from mcp_server.exceptions import ConfigurationError
from mcp_server.logger import get_logger
from mcp_server.services.providers.base import ImageProvider

logger = get_logger(__name__)


class ProviderRegistry:
    """Реестр провайдеров моделей.

    Управляет регистрацией и выбором провайдеров генерации изображений.
    Каждый провайдер инкапсулирует особенности конкретной модели.

    Attributes:
        providers: Словарь зарегистрированных провайдеров.
        _default: Имя провайдера по умолчанию.
    """

    def __init__(self) -> None:
        self.providers: dict[str, ImageProvider] = {}
        self._default: str | None = None
        logger.info("ProviderRegistry инициализирован")

    def register(
        self,
        name: str,
        provider: ImageProvider,
        default: bool = False,
    ) -> None:
        """Регистрирует провайдер.

        Args:
            name: Имя провайдера (уникальное).
            provider: Экземпляр ImageProvider.
            default: Если True, провайдер становится провайдером по умолчанию.

        Raises:
            ConfigurationError: Если провайдер с таким именем уже зарегистрирован.
        """
        if name in self.providers:
            raise ConfigurationError(f"Провайдер уже зарегистрирован: {name}")

        self.providers[name] = provider

        if default:
            self._default = name

        logger.info("Зарегистрирован провайдер: %s (default=%s)", name, default)

    def get_provider(self, name: str) -> ImageProvider | None:
        """Возвращает провайдер по имени.

        Args:
            name: Имя провайдера.

        Returns:
            ImageProvider или None, если провайдер не найден.
        """
        return self.providers.get(name)

    def get_default(self) -> ImageProvider | None:
        """Возвращает провайдер по умолчанию.

        Returns:
            ImageProvider или None, если провайдер по умолчанию не установлен.
        """
        if self._default:
            return self.providers.get(self._default)
        return None

    def list_providers(self) -> list[str]:
        """Возвращает список имён зарегистрированных провайдеров.

        Returns:
            Список имён провайдеров.
        """
        return list(self.providers.keys())

    def select_provider(
        self,
        name: str | None = None,
        vram_available: int | None = None,
    ) -> ImageProvider:
        """Выбирает провайдер по имени или доступной VRAM.

        Args:
            name: Имя провайдера. Если None — используется провайдер по умолчанию.
            vram_available: Доступный объём VRAM в ГБ. Если указан — выбирается
                           провайдер, удовлетворяющий ограничению.

        Returns:
            Выбранный ImageProvider.

        Raises:
            ConfigurationError: Если провайдер не найден.
        """
        if name:
            provider = self.providers.get(name)
            if provider is None:
                raise ConfigurationError(f"Провайдер не найден: {name}")

            if vram_available is not None and provider.vram_required > vram_available:
                raise ConfigurationError(
                    f"Провайдер {name} требует {provider.vram_required}GB VRAM, "
                    f"доступно {vram_available}GB"
                )

            return provider

        if vram_available is not None:
            for provider in self.providers.values():
                if provider.vram_required <= vram_available:
                    return provider
            raise ConfigurationError(
                f"Нет провайдеров, доступных для {vram_available}GB VRAM"
            )

        default = self.get_default()
        if default is None:
            raise ConfigurationError("Провайдер по умолчанию не установлен")

        return default
