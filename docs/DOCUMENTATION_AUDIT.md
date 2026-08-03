# DOCUMENTATION_AUDIT.md

## Аудит проектной документации

**MiMo Web Toolkit** — версия 1.0

Дата аудита: 2026-08-03

---

## Методика

Проведён сравнительный анализ всех документов проекта:

- README.md
- requirements.txt
- pyproject.toml
- config/settings.yaml
- docs/PROJECT_SPEC.md
- docs/ARCHITECTURE.md
- docs/PROJECT_STRUCTURE.md
- docs/ROADMAP.md
- docs/CODING_STANDARDS.md
- docs/CONTRIBUTING.md
- docs/AI_AGENT_GUIDE.md
- docs/MCP_TOOLS.md
- docs/COMFYUI_SETUP.md
- docs/MODEL_PROVIDERS.md
- docs/START_PROJECT_PROMPT.md

---

## Найденные проблемы

### 1. Структура mcp_server/ — три противоречащих варианта

**Важность:** КРИТИЧЕСКАЯ

**Описание:**

ARCHITECTURE.md описывает **плоскую** структуру:

```
mcp_server/
  server.py
  registry.py
  comfy_client.py
  prompt_engine.py
  workflow_engine.py
  image_tools.py
  optimizer.py
  config.py
  logger.py
  exceptions.py
```

PROJECT_STRUCTURE.md описывает **иерархическую** структуру:

```
mcp_server/
  server.py
  registry.py
  config_manager.py
  logger.py
  exceptions.py
  tools/
  services/
  models/
```

MODEL_PROVIDERS.md добавляет третий вариант:

```
mcp_server/
  services/
    providers/
      base.py
      flux_provider.py
      sdxl_provider.py
      registry.py
```

**Проблема:** три документа — три разные структуры. Агент не знает, какую использовать.

**Предлагаемое решение:** Использовать вариант из PROJECT_STRUCTURE.md как основу (иерархическая структура с tools/, services/, models/). Дополнить services/ слоем providers/ из MODEL_PROVIDERS.md. Обновить ARCHITECTURE.md.

---

### 2. Название файла конфигурации

**Важность:** СРЕДНЯЯ

**Описание:**

ARCHITECTURE.md: `config.py`
PROJECT_STRUCTURE.md: `config_manager.py`

**Проблема:** два разных имени для одного модуля.

**Предлагаемое решение:** Использовать `config_manager.py` (из PROJECT_STRUCTURE.md) — имя более описательное.

---

### 3. comfy_client.py vs providers/

**Важность:** КРИТИЧЕСКАЯ

**Описание:**

ARCHITECTURE.md говорит: «ComfyUI Client — единственная точка взаимодействия с ComfyUI. Другие компоненты не должны выполнять HTTP-запросы к ComfyUI напрямую.»

MODEL_PROVIDERS.md вводит слой `providers/`, который по смыслу тоже взаимодействует с ComfyUI (через разные модели).

**Проблема:** неясно, кто отвечает за HTTP-запросы к ComfyUI — comfy_client.py или providers?

**Предлагаемое решение:** comfy_client.py остаётся единственным HTTP-клиентом. Providers используют comfy_client.py как транспорт. Providers отвечают только за логику конкретной модели (параметры, workflow, capabilities), а не за HTTP.

---

### 4. Слой providers/ отсутствует в ROADMAP

**Важность:** СРЕДНЯЯ

**Описание:**

MODEL_PROVIDERS.md описывает архитектурный слой providers/ с base.py, flux_provider.py, sdxl_provider.py, registry.py.

ROADMAP.md не упоминает создание этого слоя ни на одном из 20 этапов.

**Проблема:** ROADMAP не отражает полную архитектуру.

**Предлагаемое решение:** Добавить создание providers/ в ROADMAP (между Этапом 5 — ComfyUI Client и Этапом 6 — generate_image tool).

---

### 5. exceptions.py vs exceptions/ пакет

**Важность:** НИЗКАЯ

**Описание:**

ARCHITECTURE.md: `exceptions.py` (один файл)
CODING_STANDARDS.md: «Создать пакет: exceptions/»

**Проблема:** неясно — один файл или пакет с несколькими модулями.

**Предлагаемое решение:** Использовать один файл `exceptions.py` в корне mcp_server/. На ранних этапах достаточно. При росте — рефакторинг в пакет.

---

### 6. queue_manager.py — упоминается не во всех документах

**Важность:** НИЗКАЯ

**Описание:**

COMFYUI_SETUP.md и PROJECT_STRUCTURE.md упоминают `queue_manager.py`.
ARCHITECTURE.md не упоминает.
ROADMAP.md не упоминает отдельным этапом.

**Проблема:** компонент существует в одних документах, но не в других.

**Предлагаемое решение:** Добавить queue_manager.py в ARCHITECTURE.md как компонент services/. ROADMAP Этап 5 (ComfyUI Client) расширить включением queue_manager.

---

### 7. Дублирование HTTP-клиентов в requirements.txt

**Важность:** НИЗКАЯ

**Описание:**

requirements.txt содержит:
- `httpx>=0.27.0`
- `requests>=2.32.0`
- `aiohttp>=3.9.5`

Три библиотеки с перекрывающимся функционалом.

**Проблема:** избыточность, путаница при выборе.

**Предлагаемое решение:** Оставить `httpx` (поддерживает sync + async, современный). Убрать `requests` и `aiohttp` или оставить один из них как fallback.

---

### 8. config/settings.yaml — неполная конфигурация

**Важность:** СРЕДНЯЯ

**Описание:**

Текущий settings.yaml:
```yaml
hardware:
  gpu:
    name: "RTX 3080"
    vram_gb: 10
  ram_gb: 32
generation:
  max_parallel_jobs: 1
  comfyui:
    low_vram: true
    cpu_offload: true
```

COMFYUI_SETUP.md ожидает:
```yaml
comfyui:
  host: 127.0.0.1
  port: 8188
  timeout: 600
```

**Проблема:** в settings.yaml отсутствуют host, port, timeout для ComfyUI.

**Предлагаемое решение:** Расширить settings.yaml секцией comfyui connection parameters.

---

### 9. MODEL_PROVIDERS.md — registry.py дублируется

**Важность:** НИЗКАЯ

**Описание:**

PROJECT_STRUCTURE.md: `mcp_server/registry.py` — регистрация MCP Tools
MODEL_PROVIDERS.md: `mcp_server/services/providers/registry.py` — регистрация providers

**Проблема:** два файла с одинаковым именем в разных контекстах может вызвать путаницу.

**Предлагаемое решение:** Переименовать `providers/registry.py` в `providers/provider_registry.py` для ясности.

---

### 10. ROADMAP — Этап 1 не упоминает requirements.txt

**Важность:** НИЗКАЯ

**Описание:**

ROADMAP Этап 1: «Создать: структуру каталогов, requirements.txt, README.md, LICENSE, .gitignore, базовую конфигурацию, систему настроек.»

requirements.txt уже создан и содержит зависимости. Этап 1 частично выполнен.

**Проблема:** ROADMAP не отражает текущее состояние.

**Предлагаемое решение:** Отметить в ROADMAP, что requirements.txt уже готов. Структура каталогов и .gitignore ещё не созданы.

---

## Сводка

| # | Проблема | Важность | Статус |
|---|----------|----------|--------|
| 1 | Структура mcp_server/ — три варианта | КРИТИЧЕСКАЯ | Требует решения |
| 2 | config.py vs config_manager.py | СРЕДНЯЯ | Требует решения |
| 3 | comfy_client.py vs providers/ | КРИТИЧЕСКАЯ | Требует решения |
| 4 | providers/ отсутствует в ROADMAP | СРЕДНЯЯ | Требует решения |
| 5 | exceptions.py vs exceptions/ | НИЗКАЯ | Рекомендация |
| 6 | queue_manager.py не везде | НИЗКАЯ | Рекомендация |
| 7 | Дублирование HTTP-клиентов | НИЗКАЯ | Рекомендация |
| 8 | settings.yaml неполная | СРЕДНЯЯ | Требует решения |
| 9 | registry.py дублируется | НИЗКАЯ | Рекомендация |
| 10 | ROADMAP не отражает состояние | НИЗКАЯ | Рекомендация |

---

## Следующий шаг

После утверждения решений по критическим проблемам — перейти к Этапу 2 (Проверка архитектуры) из START_PROJECT_PROMPT.md.
