# AGENTS.md

MCP Toolkit для локальной генерации изображений (ComfyUI + FLUX.1 Schnell) в Xiaomi MiMo Code.

## Текущее состояние

Ранняя стадия: существуют только `docs/`, `config/settings.yaml`, `pyproject.toml`, `requirements.txt` (пустой). Исходный код Python отсутствует. Каталоги `mcp_server/`, `workflows/`, `assets/`, `tests/`, `examples/` запланированы, но ещё не созданы.

## Стек

- Python 3.11+, black (line-length 88), ruff (line-length 88), mypy (3.11)
- Целевая платформа: Windows 10, NVIDIA RTX 3080 10GB VRAM, 32GB RAM
- ComfyUI + FLUX.1 Schnell работают локально (облачные сервисы запрещены)
- Протокол MCP для интеграции с MiMo Code

## Команды

```bash
python -m mcp_server.server          # запуск MCP-сервера
pip install -r requirements.txt      # установка зависимостей (пока пустой)
```

Тесты, линтер и CI пока не настроены. pyproject.toml содержит настройки black/ruff/mypy, но без скриптов и dev-зависимостей.

## Архитектура (обязательно изучить перед написанием кода)

Руководствоваться `docs/ARCHITECTURE.md`. Ключевая структура:

```
mcp_server/
  server.py          # точка входа MCP-сервера, без бизнес-логики
  registry.py        # регистрация инструментов (автообнаружение при запуске)
  tools/             # один файл = один MCP-инструмент
  services/
    comfy_client.py  # ЕДИНСТВЕННЫЙ HTTP-интерфейс к ComfyUI
    prompt_engine.py # YAML-шаблоны -> готовые промпты
    workflow_engine.py # выбор JSON-workflow для ComfyUI
    image_processor.py
  models/            # dataclass'ы для запросов/ответов
  config_manager.py  # загрузка YAML-конфигурации
  logger.py
  exceptions.py      # WorkflowError, ComfyConnectionError и т.д.
```

## Жёсткие правила

- **Только pathlib** -- `os.path` запрещён
- **YAML для конфигурации/промптов/workflow** -- никаких захардкоженных путей, размеров, промптов или JSON-workflow в Python-коде
- **Доступ к ComfyUI** только через `comfy_client.py`. Ни один другой модуль не делает HTTP-запросов к ComfyUI
- **Шаблоны промптов** хранятся в `config/prompts.yaml`. Изменение качества генерации не должно требовать правки Python-кода
- **Workflow** хранятся как JSON-файлы в `workflows/`, а не встраиваются в код
- **Логирование**: модуль `logging` с именованными логгерами, `print()` запрещён
- **Type hints** на всех публичных функциях
- **Dataclass'ы** для структурированных данных (ImageRequest, WorkflowInfo и т.д.)
- Pydantic только там, где валидация входных данных действительно нужна
- Каждый MCP-инструмент = один независимый модуль с одной ответственностью
- Запрещены `except: pass`, заглушки/TODO без объяснений, псевдокод
- Файлы: ~300 строк — отлично, до 500 — допустимо. Функции: 10-30 строк

## Контракт MCP-инструментов

Все инструменты возвращают `{ "success": bool, "result": ..., "error": {"type": str, "message": str} | null }`.

12 инструментов запланировано: `generate_image`, `generate_logo`, `generate_icons`, `generate_background`, `generate_team_photo`, `generate_product_image`, `remove_background`, `optimize_image`, `upscale_image`, `describe_image`, `create_favicon`, `convert_svg`. Схемы — в `docs/MCP_TOOLS.md`.

`generate_image` использует высокоуровневый интерфейс (`purpose`, `subject`, `style`, `aspect_ratio`), который внутри сам выбирает шаблон промпта, workflow, разрешение, sampler, scheduler, CFG, steps и negative prompt.

## Порядок разработки

Следовать поэтапному плану в `docs/ROADMAP.md`. Каждый этап завершается полностью рабочим состоянием. Никогда не пропускать этапы.

### Цикл реализации этапа

1. **Plan-агент**: архитектурное решение + план этапа
2. **Build-агент**: реализация по плану
3. **Plan-агент**: архитектурный контроль реализации
4. **Коммит** (по запросу пользователя)
5. **Следующий этап**

### Формат документирования этапа

После завершения каждого этапа вывести в чат:

1. Архитектурное решение (что и почему)
2. Созданные файлы
3. Изменённые файлы
4. Дерево файлов (если структура изменилась)
5. Проверка соответствия архитектуре

### Правила

- Перед каждым этапом: объяснить архитектурное решение, показать дерево файлов
- После завершения этапа: перечислить файлы, описать результат
- Если обнаружено более удачное архитектурное решение — объяснить, предложить, только после согласования изменить
- Нет функциональности из последующих этапов — строгий scope по текущему этапу

## Указатель документации

Вся документация в `docs/`:

| Файл | Назначение |
|------|------------|
| PROJECT_SPEC.md | Требования, ограничения, планка качества |
| ARCHITECTURE.md | Компоненты, потоки данных, принципы |
| ROADMAP.md | План из 22 этапов, соблюдать порядок |
| IMPLEMENTATION_PLAN.md | Детальный план реализации по этапам |
| PROJECT_STATUS.md | Текущий статус, Architecture Freeze v1.0 |
| CODING_STANDARDS.md | Стиль, именование, импорты, исключения |
| CONTRIBUTING.md | Порядок внесения изменений, правила для AI-агентов |
| AI_AGENT_GUIDE.md | Правила поведения агентов, запрещённые действия |
| MCP_TOOLS.md | Схемы и контракты инструментов |
| PROJECT_STRUCTURE.md | Расположение файлов и каталогов |
| COMFYUI_SETUP.md | Установка ComfyUI |
| MODEL_PROVIDERS.md | Информация о провайдерах моделей |
