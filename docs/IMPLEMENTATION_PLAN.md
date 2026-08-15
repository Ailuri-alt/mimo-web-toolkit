# IMPLEMENTATION_PLAN.md

## План реализации

**MiMo Web Toolkit**

Версия: 1.0

Дата: 2026-08-03

Основание: ROADMAP.md, ARCHITECTURE_REVIEW.md

---

## Статус архитектуры

**Architecture Freeze v1.0**

---

## Подготовительный этап (перед ROADMAP Этап 1)

### 1. Создание структуры каталогов

```bash
mkdir mcp_server
mkdir mcp_server/tools
mkdir mcp_server/services
mkdir mcp_server/services/providers
mkdir mcp_server/services/comfy
mkdir mcp_server/models
mkdir workflows
mkdir workflows/flux
mkdir assets
mkdir assets/generated
mkdir assets/optimized
mkdir assets/cache
mkdir cache
mkdir tests
mkdir examples
mkdir scripts
```

### 2. Создание .gitignore

Исключить:

* venv/
* __pycache__/
* *.pyc
* .env
* assets/generated/
* assets/cache/
* logs/
* .mypy_cache/
* .ruff_cache/

### 3. Настройка Python-окружения

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Проверка установки

```bash
python -c "import mcp; print(mcp.__version__)"
black --version
ruff --version
mypy --version
```

---

## ROADMAP Этап 1 — Каркас проекта

Файлы:

* mcp_server/__init__.py
* mcp_server/server.py (заглушка)
* mcp_server/config_manager.py (заглушка)
* mcp_server/logger.py (заглушка)
* mcp_server/exceptions.py (заглушка)

Результат: проект запускается без ошибок.

---

## ROADMAP Этап 2 — Конфигурация

Файлы:

* config/settings.yaml (расширенная версия)
* config/prompts.yaml
* config/workflows.yaml

Реализовать:

* config_manager.py — загрузка YAML, валидация, предоставление настроек

---

## ROADMAP Этап 3 — Логирование

Файлы:

* mcp_server/logger.py

Реализовать:

*_named loggers
* уровни INFO, WARNING, ERROR, DEBUG
* сохранение в logs/

---

## ROADMAP Этап 4 — MCP Server

Файлы:

* mcp_server/server.py
* mcp_server/registry.py

Реализовать:

* запуск MCP Server
* регистрация инструментов
* обработку запросов

Результат: MiMo Code подключается к серверу.

---

## ROADMAP Этап 5 — ComfyUI Client

Файлы:

* mcp_server/services/comfy/comfy_client.py
* mcp_server/services/queue_manager.py

Реализовать:

* отправку workflow
* получение ID задачи
* отслеживание выполнения
* получение результата
* очередь генерации (max 1 job)

---

## ROADMAP Этап 6 — Provider Layer

Файлы:

* mcp_server/services/providers/__init__.py
* mcp_server/services/providers/base.py
* mcp_server/services/providers/flux_provider.py
* mcp_server/services/providers/provider_registry.py

Реализовать:

* интерфейс ImageProvider (generate, validate, get_capabilities)
* FluxProvider для FLUX.1 Schnell/Dev
* реестр провайдеров

Правило: Provider использует comfy_client.py, никогда не делает HTTP напрямую.

---

## ROADMAP Этап 7 — Tool generate_image

Файлы:

* mcp_server/tools/generate_image.py
* mcp_server/models/image_request.py
* mcp_server/models/image_response.py

Реализовать:

* высокоуровневый интерфейс (purpose, subject, style, aspect_ratio)
* выбор prompt template
* выбор workflow
* запуск генерации через Provider
* возврат пути к файлу

Результат: первая генерация изображения.

---

## ROADMAP Этап 8 — Prompt Engine

Файлы:

* mcp_server/services/prompt_engine.py

Реализовать:

* загрузку шаблонов из config/prompts.yaml
* формирование промпта по purpose/style

---

## ROADMAP Этап 9 — Workflow Engine

Файлы:

* mcp_server/services/workflow_engine.py

Реализовать:

* выбор workflow по purpose/style/aspect_ratio
* загрузку JSON из workflows/flux/

---

## ROADMAP Этап 10 — Image Optimizer

Файлы:

* mcp_server/services/image_processor.py

Реализовать:

* конвертацию в WebP/PNG/JPG
* оптимизацию размера
* масштабирование изображений (resize, LANCZOS-интерполяция)
* сохранение в assets/optimized/

---

## ROADMAP Этапы 11-19 — Остальные MCP Tools

Файлы:

* mcp_server/tools/generate_logo.py
* mcp_server/tools/generate_icons.py
* mcp_server/tools/generate_background.py
* mcp_server/tools/generate_team_photo.py
* mcp_server/tools/generate_product_image.py
* mcp_server/tools/remove_background.py
* mcp_server/tools/upscale_image.py
* mcp_server/tools/describe_image.py
* mcp_server/tools/create_favicon.py
* mcp_server/tools/convert_svg.py

Каждый инструмент — отдельный модуль.

---

## ROADMAP Этап 20 — Интеграция с MiMo Code

Проверить:

* регистрацию MCP
* вызов всех инструментов
* возврат результатов
* обработку ошибок

---

## ROADMAP Этап 21 — Примеры

Каталог examples/:

* landing_page/
* ecommerce/
* portfolio/

---

## ROADMAP Этап 22 — Финальная подготовка

* документация
* тесты
* производительность
* публикация на GitHub

---

## Порядок реализации

1. Подготовительный этап
2. Этап 1 (каркас)
3. Этап 2 (конфигурация)
4. Этап 3 (логирование)
5. Этап 4 (MCP Server)
6. Этап 5 (ComfyUI Client)
7. Этап 6 (Provider Layer)
8. Этап 7 (generate_image)
9. Этапы 8-10 (движки)
10. Этапы 11-19 (остальные tools)
11. Этап 20 (интеграция)
12. Этапы 21-22 (примеры, финал)

---

## Запрещено

* пропускать этапы
* начинать следующий этап до завершения предыдущего
* менять архитектуру без согласования
* использовать заглушки без объяснения
