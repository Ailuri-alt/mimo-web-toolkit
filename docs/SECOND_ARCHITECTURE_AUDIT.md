# SECOND_ARCHITECTURE_AUDIT.md

## Контрольный аудит согласованности

**MiMo Web Toolkit**

Дата: 2026-08-11

---

## 1. Полный список MCP Tools (MCP_TOOLS.md)

| # | Инструмент | Назначение |
|---|------------|------------|
| 1 | generate_image | Универсальная генерация изображений |
| 2 | generate_logo | Создание логотипов |
| 3 | generate_icons | Создание набора иконок |
| 4 | generate_background | Создание фоновых изображений |
| 5 | generate_team_photo | Генерация изображений людей/команд |
| 6 | generate_product_image | Создание изображений товаров |
| 7 | remove_background | Удаление фона |
| 8 | optimize_image | Оптимизация изображений |
| 9 | upscale_image | Увеличение разрешения |
| 10 | describe_image | Анализ изображения |
| 11 | create_favicon | Создание favicon |
| 12 | convert_svg | Работа с SVG |

---

## 2. Порядок реализации (ROADMAP.md)

| Этап | Инструмент | Статус |
|------|------------|--------|
| 1-5 | Инфраструктура | ✓ Завершено |
| 6 | Provider Layer | ✓ Завершено |
| 7 | generate_image | ✓ Завершено |
| 8 | Prompt Engine | ✓ Завершено |
| 9 | Workflow Engine | ✓ Завершено |
| 10 | Image Optimizer | ✓ Завершено |
| 11 | generate_logo | ✓ Завершено |
| 12 | generate_icons | ✓ Завершено |
| 13 | generate_background | ✓ Завершено |
| 14 | generate_team_photo | ✓ Завершено |
| 15 | generate_product_image | ✓ Завершено |
| 16 | remove_background | ✓ Завершено |
| 17 | upscale_image | ✓ Завершено |
| 18 | describe_image | ✓ Завершено |
| 19 | create_favicon | ✗ Не реализован |
| 20 | Интеграция с MiMo Code | ✗ Не реализован |
| 21 | Примеры | ✗ Не реализован |
| 22 | Финальная подготовка | ✗ Не реализован |

---

## 3. IMPLEMENTATION_PLAN.md vs ROADMAP.md

| Проверка | Результат |
|----------|-----------|
| Этапы 1-10 | Совпадают |
| Этапы 11-19 | IMPLEMENTATION_PLAN объединяет их в группу «Остальные MCP Tools» |
| create_favicon | ROADMAP: Этап 19, IMPLEMENTATION_PLAN: Этапы 11-19 |
| convert_svg | ROADMAP: не указан отдельным этапом, IMPLEMENTATION_PLAN: Этапы 11-19 |
| optimize_image | ROADMAP: не указан, IMPLEMENTATION_PLAN: не указан |

---

## 4. Фактически реализованные инструменты

| Инструмент | Файл | Зарегистрирован |
|------------|------|-----------------|
| generate_image | ✓ | ✓ |
| generate_logo | ✓ | ✓ |
| generate_icons | ✓ | ✓ |
| generate_background | ✓ | ✓ |
| generate_team_photo | ✓ | ✓ |
| generate_product_image | ✓ | ✓ |
| remove_background | ✓ | ✓ |
| upscale_image | ✓ | ✓ |
| describe_image | ✓ | ✓ |

---

## 5. Отсутствующие инструменты

| Инструмент | В MCP_TOOLS.md | В ROADMAP | В IMPLEMENTATION_PLAN |
|------------|----------------|-----------|----------------------|
| optimize_image | ✓ | ✗ | ✗ |
| create_favicon | ✓ | ✓ (Этап 19) | ✓ (Этапы 11-19) |
| convert_svg | ✓ | ✗ | ✓ (Этапы 11-19) |

---

## 6. Соответствие инструментов существующим сервисам

| Инструмент | PromptEngine | WorkflowEngine | Provider | ComfyClient | ImageProcessor |
|------------|--------------|----------------|----------|-------------|----------------|
| generate_image | ✓ | ✓ | ✓ | ✓ | ✗ |
| generate_logo | ✓ | ✓ | ✓ | ✓ | ✗ |
| generate_icons | ✓ | ✓ | ✓ | ✓ | ✗ |
| generate_background | ✓ | ✓ | ✓ | ✓ | ✗ |
| generate_team_photo | ✓ | ✓ | ✓ | ✓ | ✗ |
| generate_product_image | ✓ | ✓ | ✓ | ✓ | ✗ |
| remove_background | ✗ | ✗ | ✗ | ✗ | ✓ |
| upscale_image | ✗ | ✗ | ✗ | ✗ | ✗ |
| describe_image | ✗ | ✗ | ✗ | ✗ | ✓ |

---

## 7. Реалистичность ImageProcessor

| Формат | Поддержка | Примечание |
|--------|-----------|------------|
| WebP | ✓ | Pillow |
| PNG | ✓ | Pillow |
| JPG/JPEG | ✓ | Pillow |
| AVIF | ✗ | Требует pillow-avif-plugin |

---

## 8. describe_image — AI-анализ изображения

### Что означает «AI-анализ изображения»

В текущей реализации describe_image возвращает только **техническую метаинформацию**:

* format, mode, width, height, size_bytes
* alt_text и title генерируются из имени файла

**Настоящий AI-анализ** подразумевает:

* распознавание объектов на изображении;
* генерацию текстового описания содержимого;
* определение сцены, стиля, настроения;
* создание осмысленного alt-text.

### Необходимые компоненты для AI-анализа

| Компонент | Назначение | Статус |
|-----------|------------|--------|
| Vision Provider | Интеграция с vision-моделью (GPT-4V, Claude Vision, локальная модель) | ✗ Отсутствует |
| Vision Service | Обработка запросов к vision-модели | ✗ Отсутствует |
| API для vision-модели | HTTP-клиент для внешнего сервиса | ✗ Отсутствует |

### Вывод

Текущая реализация describe_image **не выполняет AI-анализ**. Для его реализации необходим:

1. Vision Provider (новый компонент в providers/)
2. Vision Service (новый компонент в services/)
3. Интеграция с внешним vision API или локальной моделью

---

## 9. optimize_image, create_favicon, convert_svg

### optimize_image

| Параметр | Значение |
|----------|----------|
| Должен быть отдельным MCP Tool | Да |
| Этап ROADMAP | Не указан (рекомендуется между 18 и 19) |
| Существующий сервис | ImageProcessor.process() |
| Форматы | WebP, PNG, JPG (AVIF требует pillow-avif-plugin) |

### create_favicon

| Параметр | Значение |
|----------|----------|
| Должен быть отдельным MCP Tool | Да |
| Этап ROADMAP | 19 |
| Существующий сервис | ImageProcessor.process() |
| Входные данные | source (путь к SVG/PNG) |

### convert_svg

| Параметр | Значение |
|----------|----------|
| Должен быть отдельным MCP Tool | Да |
| Этап ROADMAP | Не указан (рекомендуется после create_favicon) |
| Существующий сервис | ImageProcessor + cairosvg |
| Поддержка | PNG→SVG, SVG→PNG, SVG→WebP |

---

## 10. Подтверждённые требования

| # | Требование | Источник |
|---|------------|----------|
| 1 | 12 MCP Tools | MCP_TOOLS.md |
| 2 | Каждый инструмент — отдельный модуль | IMPLEMENTATION_PLAN.md |
| 3 | Инструменты используют архитектурные компоненты | ARCHITECTURE.md |
| 4 | ImageProcessor — единственный обработчик изображений | ARCHITECTURE.md |
| 5 | ComfyClient — единственный HTTP-слой | ARCHITECTURE.md |

---

## 11. Реальные несоответствия

| # | Несоответствие | Важность |
|---|----------------|----------|
| 1 | optimize_image отсутствует в ROADMAP | СРЕДНЯЯ |
| 2 | convert_svg отсутствует в ROADMAP | СРЕДНЯЯ |
| 3 | AVIF не поддерживается в ImageProcessor | НИЗКАЯ |
| 4 | describe_image не выполняет AI-анализ | ВЫСОКАЯ |
| 5 | upscale_image не использует ImageProcessor | НИЗКАЯ |

---

## 12. Предложения MiMo

| # | Предложение | Обоснование |
|---|-------------|-------------|
| 1 | Добавить optimize_image в ROADMAP между Этапами 18 и 19 | MCP_TOOLS.md требует этот инструмент |
| 2 | Добавить convert_svg в ROADMAP после create_favicon | MCP_TOOLS.md требует этот инструмент |
| 3 | Рассмотреть добавление pillow-avif-plugin | MCP_TOOLS.md указывает AVIF |
| 4 | Зафиксировать отсутствие AI-анализа в describe_image | Необходим Vision Provider |
| 5 | Рефакторить upscale_image для использования ImageProcessor | Консистентность архитектуры |

---

## 13. Вопросы, требующие архитектурного решения

| # | Вопрос | Варианты |
|---|--------|----------|
| 1 | Добавить ли optimize_image в ROADMAP? | Да / Нет |
| 2 | Добавить ли convert_svg в ROADMAP? | Да / Нет |
| 3 | Добавить ли поддержку AVIF в ImageProcessor? | Да / Нет |
| 4 | Реализовать ли AI-анализ в describe_image? | Да / Нет |
| 5 | Если да — какой Vision Provider использовать? | GPT-4V / Claude Vision / Локальная модель |
| 6 | Рефакторить ли upscale_image? | Да / Нет |
