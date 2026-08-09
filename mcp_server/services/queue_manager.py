"""Менеджер очереди генерации изображений.

Управляет очередью задач генерации.
Одновременно выполняется не более 1 задачи (ограничение RTX 3080 10GB).
"""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from mcp_server.logger import get_logger

logger = get_logger(__name__)

DEFAULT_MAX_JOBS = 1


class QueueManager:
    """Менеджер очереди генерации.

    Управляет выполнением задач генерации изображений.
    Гарантирует, что одновременно выполняется не более max_jobs задач.

    Attributes:
        max_jobs: Максимальное количество одновременных задач.
        _semaphore: Семафор для ограничения параллельных задач.
        _queue: Очередь ожидающих задач.
    """

    def __init__(self, max_jobs: int = DEFAULT_MAX_JOBS) -> None:
        """Инициализирует менеджер очереди.

        Args:
            max_jobs: Максимальное количество одновременных задач.
                      По умолчанию 1 (ограничение RTX 3080 10GB).
        """
        self.max_jobs = max_jobs
        self._semaphore = asyncio.Semaphore(max_jobs)
        self._queue: list[str] = []
        logger.info("QueueManager инициализирован: max_jobs=%d", max_jobs)

    async def execute(
        self,
        task_id: str,
        func: Callable[..., Awaitable[Any]],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Выполняет задачу в очереди.

        Если все слоты заняты, задача ждёт освобождения.

        Args:
            task_id: Идентификатор задачи (для логирования).
            func: Асинхронная функция для выполнения.
            *args: Позиционные аргументы функции.
            **kwargs: Именованные аргументы функции.

        Returns:
            Результат выполнения функции.
        """
        async with self._semaphore:
            self._queue.append(task_id)
            logger.info(
                "Задача начата: %s (в очереди: %d)",
                task_id,
                len(self._queue),
            )

            try:
                result = await func(*args, **kwargs)
                logger.info("Задача завершена: %s", task_id)
                return result
            finally:
                self._queue.remove(task_id)
                logger.info(
                    "Задача удалена из очереди: %s (в очереди: %d)",
                    task_id,
                    len(self._queue),
                )

    @property
    def pending_count(self) -> int:
        """Количество ожидающих задач."""
        return len(self._queue)

    @property
    def available_slots(self) -> int:
        """Количество доступных слотов."""
        return self.max_jobs - self.pending_count
