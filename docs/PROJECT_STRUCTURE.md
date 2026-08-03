# PROJECT_STRUCTURE.md

# MiMo Web Toolkit

## Структура проекта

Версия: 1.0

---

# Назначение документа

Этот документ описывает физическую структуру репозитория **MiMo Web Toolkit**.

Он используется:

* разработчиками;
* AI-агентами;
* инструментами автоматической генерации кода.

Главная цель — сохранить понятную и предсказуемую организацию проекта.

---

# Общая структура

```text
mimo-web-toolkit/

│
├── README.md
├── AI_CONTEXT.md
├── AGENTS.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── pyproject.toml
│
├── docs/
│
├── config/
│
├── mcp_server/
│
├── workflows/
│
├── assets/
│
├── cache/
│
├── examples/
│
├── tests/
│
└── scripts/
```

---

# Корневые файлы

## README.md

Назначение:

Главная документация проекта.

Содержит:

* описание;
* установку;
* запуск;
* примеры;
* ссылки на документацию.

Не содержит:

* внутренние архитектурные детали;
* большой технический код.

---

## LICENSE

Лицензия проекта.

Определяет правила использования и распространения.

---

## .gitignore

Содержит исключения Git.

Должен исключать:

* виртуальные окружения;
* временные файлы;
* кэш;
* логи;
* сгенерированные изображения.

---

## requirements.txt

Список Python-зависимостей.

Все новые библиотеки должны добавляться осознанно.

---

## pyproject.toml

Основная конфигурация Python-проекта.

Содержит:

* метаданные проекта;
* настройки инструментов разработки;
* настройки форматирования и проверки.

---

# Каталог docs/

## Назначение

Документация проекта.

Структура:

```text
docs/

├── PROJECT_SPEC.md
├── ARCHITECTURE.md
├── PROJECT_STRUCTURE.md
├── ROADMAP.md
├── CODING_STANDARDS.md
├── CONTRIBUTING.md
├── AI_AGENT_GUIDE.md
└── MCP_TOOLS.md
```

---

## PROJECT_SPEC.md

Описание:

Что должен делать проект.

Содержит:

* цели;
* требования;
* ограничения;
* сценарии использования.

---

## ARCHITECTURE.md

Описание:

Как устроена система.

Содержит:

* компоненты;
* связи;
* потоки данных;
* архитектурные решения.

---

## PROJECT_STRUCTURE.md

Текущий документ.

Описание:

Где находятся файлы проекта.

---

## ROADMAP.md

Описание:

План разработки.

Содержит:

* этапы;
* порядок реализации;
* критерии завершения.

---

## CODING_STANDARDS.md

Описание:

Правила написания кода.

Содержит:

* стиль;
* архитектурные ограничения;
* требования к качеству.

---

## CONTRIBUTING.md

Описание:

Правила внесения изменений.

---

## AI_AGENT_GUIDE.md

Описание:

Правила работы AI-разработчиков.

---

## MCP_TOOLS.md

Описание:

Контракт MCP-инструментов.

---

# Каталог config/

## Назначение

Все настройки проекта.

Структура:

```text
config/

├── settings.yaml
├── prompts.yaml
└── workflows.yaml
```

---

## settings.yaml

Содержит:

* параметры сервера;
* пути;
* настройки ComfyUI;
* настройки оборудования.

Пример:

```yaml
hardware:
  gpu:
    name: "RTX 3080"
    vram_gb: 10
  ram_gb: 32

comfyui:
  host: "127.0.0.1"
  port: 8188
  timeout: 600
  low_vram: true
  cpu_offload: true

generation:
  max_parallel_jobs: 1
```

---

## prompts.yaml

Содержит:

* шаблоны prompt;
* negative prompt;
* стили генерации.

---

## workflows.yaml

Содержит:

* соответствие задачи и workflow.

---

# Каталог mcp_server/

## Назначение

Основной код MCP Server.

Структура:

```text
mcp_server/

├── server.py
├── registry.py
├── config_manager.py
├── logger.py
├── exceptions.py
│
├── tools/
│
├── services/
│
└── models/
```

---

# server.py

Отвечает за:

* запуск MCP Server;
* обработку соединений;
* регистрацию инструментов.

Не содержит:

* логику генерации изображений.

---

# registry.py

Отвечает за:

* регистрацию MCP Tools;
* управление доступными инструментами.

---

# tools/

Содержит MCP-инструменты.

Пример:

```text
tools/

├── generate_image.py
├── generate_logo.py
├── optimize_image.py
└── describe_image.py
```

Каждый файл:

* один инструмент;
* одна ответственность.

---

# services/

Содержит внутренние сервисы.

Структура:

```text
services/

├── providers/
│   ├── __init__.py
│   ├── base.py
│   ├── flux_provider.py
│   ├── sdxl_provider.py
│   └── provider_registry.py
│
├── comfy/
│   └── comfy_client.py
│
├── prompt_engine.py
├── workflow_engine.py
├── image_processor.py
└── queue_manager.py
```

---

---

## comfy_client.py

Единая точка связи с ComfyUI.

---

## prompt_engine.py

Работа с шаблонами prompt.

---

## workflow_engine.py

Выбор workflow.

---

## image_processor.py

Обработка изображений.

---

## queue_manager.py

Управление очередью генерации.

Особенно важно для RTX 3080 10 GB.

---

# models/

Содержит структуры данных.

Например:

```text
models/

├── image_request.py
└── image_response.py
```

---

# Каталог workflows/

## Назначение

Хранение ComfyUI workflow.

Структура:

```text
workflows/

└── flux/

    ├── hero.json
    ├── product.json
    ├── portrait.json
    └── background.json
```

Workflow не должны находиться внутри Python-кода.

---

# Каталог assets/

## Назначение

Рабочие данные изображений.

Структура:

```text
assets/

├── generated/
├── optimized/
└── cache/
```

---

## generated/

Исходные результаты генерации.

---

## optimized/

Финальные изображения для сайтов.

---

## cache/

Временное хранилище.

---

# Каталог examples/

## Назначение

Демонстрационные проекты.

Примеры:

```text
examples/

├── landing_page/
├── ecommerce/
└── portfolio/
```

---

# Каталог tests/

## Назначение

Автоматические тесты.

Примеры:

```text
tests/

├── test_config.py
├── test_prompt_engine.py
└── test_tools.py
```

---

# Каталог scripts/

## Назначение

Вспомогательные скрипты.

Примеры:

```text
scripts/

├── start_server.py
└── check_environment.py
```

---

# Правила размещения новых файлов

Перед созданием нового файла необходимо определить:

1. К какому компоненту он относится.
2. Может ли использоваться существующий модуль.
3. Не нарушает ли он текущую архитектуру.

---

# Запрещается

Не допускается:

* создавать файлы в корне без необходимости;
* создавать папки с непонятным назначением;
* дублировать функциональность;
* хранить конфигурацию внутри Python-кода;
* хранить workflow внутри исходников.

---

# Изменение структуры проекта

Любое изменение структуры требует:

1. обновления данного документа;
2. проверки ARCHITECTURE.md;
3. проверки документации README.md.

---

# Главная цель

Поддерживать проект организованным, понятным и удобным для совместной работы людей и AI-агентов.
