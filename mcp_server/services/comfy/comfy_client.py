"""ComfyUI Client — единственная точка взаимодействия с ComfyUI.

Отвечает за:
- отправку workflow;
- ожидание результата;
- получение изображения;
- обработку ошибок;
- контроль времени ожидания.

Другие компоненты не должны выполнять HTTP-запросы к ComfyUI напрямую.
"""

import asyncio
from pathlib import Path
from typing import Any

import httpx

from mcp_server.exceptions import ComfyConnectionError, ComfyRequestError
from mcp_server.logger import get_logger

logger = get_logger(__name__)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8188
DEFAULT_TIMEOUT = 600


class ComfyClient:
    """HTTP-клиент для взаимодействия с ComfyUI API.

    Единственный компонент системы, выполняющий HTTP-запросы к ComfyUI.
    Все остальные модули используют этот класс для работы с ComfyUI.

    Attributes:
        base_url: Базовый URL ComfyUI API.
        timeout: Таймаут запросов в секундах.
        _client: Экземпляр httpx.AsyncClient.
    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Инициализирует ComfyUI Client.

        Args:
            host: Хост ComfyUI (по умолчанию 127.0.0.1).
            port: Порт ComfyUI (по умолчанию 8188).
            timeout: Таймаут запросов в секундах (по умолчанию 600).
        """
        self.base_url = f"http://{host}:{port}"
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )
        logger.info(
            "ComfyClient инициализирован: %s (timeout=%ds)",
            self.base_url,
            timeout,
        )

    async def health_check(self) -> bool:
        """Проверяет доступность ComfyUI.

        Returns:
            True, если ComfyUI доступен, иначе False.
        """
        try:
            response = await self._client.get("/system_stats")
            return response.status_code == 200
        except httpx.HTTPError as e:
            logger.warning("ComfyUI недоступен: %s", e)
            return False

    async def queue_prompt(self, workflow: dict[str, Any]) -> str:
        """Отправляет workflow в очередь генерации.

        Args:
            workflow: JSON-workflow для ComfyUI.

        Returns:
            ID задачи (prompt_id).

        Raises:
            ComfyConnectionError: Если не удалось подключиться к ComfyUI.
            ComfyRequestError: Если ComfyUI вернул ошибку.
        """
        payload = {"prompt": workflow}

        try:
            response = await self._client.post("/prompt", json=payload)
        except httpx.HTTPError as e:
            raise ComfyConnectionError(
                f"Ошибка подключения к ComfyUI: {e}"
            ) from e

        if response.status_code != 200:
            raise ComfyRequestError(
                f"ComfyUI вернул ошибку: {response.status_code}",
                status_code=response.status_code,
            )

        data = response.json()
        prompt_id = data.get("prompt_id")

        if not prompt_id:
            raise ComfyRequestError(
                "ComfyUI не вернул prompt_id",
                status_code=response.status_code,
            )

        logger.info("Workflow отправлен: prompt_id=%s", prompt_id)
        return prompt_id

    async def get_history(self, prompt_id: str) -> dict[str, Any]:
        """Получает историю выполнения задачи.

        Args:
            prompt_id: ID задачи.

        Returns:
            Словарь с информацией о выполнении.

        Raises:
            ComfyConnectionError: Если не удалось подключиться к ComfyUI.
            ComfyRequestError: Если ComfyUI вернул ошибку.
        """
        try:
            response = await self._client.get(f"/history/{prompt_id}")
        except httpx.HTTPError as e:
            raise ComfyConnectionError(
                f"Ошибка подключения к ComfyUI: {e}"
            ) from e

        if response.status_code != 200:
            raise ComfyRequestError(
                f"ComfyUI вернул ошибку: {response.status_code}",
                status_code=response.status_code,
            )

        return response.json()

    async def wait_for_completion(
        self,
        prompt_id: str,
        poll_interval: float = 1.0,
    ) -> dict[str, Any]:
        """Ожидает завершения генерации.

        Периодически опрашивает ComfyUI до завершения задачи.
        Прерывается по таймауту (self.timeout).

        Args:
            prompt_id: ID задачи.
            poll_interval: Интервал опроса в секундах (по умолчанию 1.0).

        Returns:
            Словарь с результатом генерации.

        Raises:
            ComfyRequestError: Если задача не завершилась за timeout.
        """
        logger.info("Ожидание завершения: prompt_id=%s (timeout=%ds)", prompt_id, self.timeout)

        elapsed = 0.0
        while elapsed < self.timeout:
            history = await self.get_history(prompt_id)

            if prompt_id in history:
                entry = history[prompt_id]
                outputs = entry.get("outputs", {})

                if outputs:
                    logger.info("Генерация завершена: prompt_id=%s (%.1fs)", prompt_id, elapsed)
                    return entry

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise ComfyRequestError(
            f"Задача {prompt_id} не завершилась за {self.timeout}с",
            status_code=408,
        )

    async def get_image(
        self,
        filename: str,
        subfolder: str = "",
        folder_type: str = "output",
    ) -> bytes:
        """Загружает изображение из ComfyUI.

        Args:
            filename: Имя файла изображения.
            subfolder: Подкаталог (по умолчанию пустой).
            folder_type: Тип каталога (output/input/temp).

        Returns:
            Байты изображения.

        Raises:
            ComfyConnectionError: Если не удалось подключиться к ComfyUI.
            ComfyRequestError: Если ComfyUI вернул ошибку.
        """
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type,
        }

        try:
            response = await self._client.get("/view", params=params)
        except httpx.HTTPError as e:
            raise ComfyConnectionError(
                f"Ошибка подключения к ComfyUI: {e}"
            ) from e

        if response.status_code != 200:
            raise ComfyRequestError(
                f"Не удалось загрузить изображение: {response.status_code}",
                status_code=response.status_code,
            )

        logger.info("Изображение загружено: %s", filename)
        return response.content

    async def close(self) -> None:
        """Закрывает соединение с ComfyUI."""
        await self._client.aclose()
        logger.info("ComfyClient закрыт")
