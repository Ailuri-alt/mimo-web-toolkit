# AI_CONTEXT.md

## MiMo Web Toolkit

Единая точка входа для AI-агентов.

---

## Назначение проекта

Локальный MCP Toolkit для Xiaomi MiMo Code, позволяющий автоматически генерировать и обрабатывать изображения при разработке веб-сайтов через ComfyUI + FLUX.1 Schnell.

---

## Статус архитектуры

**Architecture Freeze v1.0**

Архитектура зафиксирована. Изменения — только через отдельные архитектурные решения.

---

## Обязательные документы перед работой

1. `AI_CONTEXT.md` — данный файл, точка входа
2. `AGENTS.md` — правила для AI-агентов
3. `docs/PROJECT_SPEC.md` — требования и ограничения
4. `docs/ARCHITECTURE.md` — компоненты и потоки данных
5. `docs/PROJECT_STRUCTURE.md` — расположение файлов
6. `docs/ROADMAP.md` — план из 22 этапов
7. `docs/CODING_STANDARDS.md` — стиль и правила кода
8. `docs/MCP_TOOLS.md` — контракты инструментов
9. `docs/MODEL_PROVIDERS.md` — слой провайдеров моделей

---

## Ключевые архитектурные правила

* Только `pathlib` — `os.path` запрещён
* YAML для конфигурации, промптов, workflow
* HTTP-запросы к ComfyUI только через `comfy_client.py`
* Provider никогда не выполняет HTTP-запросы
* Каждый MCP-инструмент — отдельный модуль
* Направление зависимостей: Tools → Services → Providers → Comfy Client → HTTP → ComfyUI

---

## Структура mcp_server/

```
mcp_server/
    server.py
    registry.py
    config_manager.py
    logger.py
    exceptions.py
    tools/
    services/
        providers/
        comfy/
        prompt_engine.py
        workflow_engine.py
        image_processor.py
        queue_manager.py
    models/
```

---

## Стек

* Python 3.11+
* black (line-length 88), ruff (line-length 88), mypy (3.11)
* Windows 10, NVIDIA RTX 3080 10GB VRAM, 32GB RAM
* ComfyUI + FLUX.1 Schnell (локально, без облака)
* MCP protocol

---

## Команды

```bash
python -m mcp_server.server
pip install -r requirements.txt
```

---

## Документация

Все файлы в `docs/`. Подробнее — в `AGENTS.md`.
