# MODEL_PROVIDERS.md

# Model Providers Specification

## MiMo Web Toolkit

Версия: 1.0

---

# Назначение

Этот документ описывает архитектуру подключения моделей генерации изображений в проекте **MiMo Web Toolkit**.

Главная задача:

обеспечить возможность замены и добавления моделей без изменения MCP-интерфейса и основной логики приложения.

---

# Основной принцип

Модель генерации является заменяемым компонентом.

MiMo Web Toolkit не должен зависеть от конкретной модели.

Неправильно:

```text id="z2p7a1"
generate_image()

        |
        |
     FLUX.1 Schnell
```

Правильно:

```text id="s9d0xk"
generate_image()

        |
        |
 Image Provider Interface

        |
        |
 +-------------+-------------+
 |             |             |
FLUX Schnell  FLUX Dev    SDXL
             NF4/GGUF
```

---

# Архитектурный уровень Provider

Provider отвечает за взаимодействие с конкретной моделью.

Он скрывает:

* название модели;
* формат файлов;
* параметры запуска;
* особенности VRAM;
* специальные настройки.

---

# Интерфейс Provider

Каждый Provider должен реализовывать:

```python
generate()

validate()

get_capabilities()

```

---

# Пример интерфейса

```python
class ImageProvider:

    def generate(
        self,
        prompt,
        workflow,
        parameters
    ):
        pass


    def validate(self):
        pass


    def get_capabilities(self):
        pass
```

---

# Структура каталогов

В проект добавляется:

```text
mcp_server/

└── services/

    └── providers/

        ├── __init__.py
        ├── base.py
        ├── flux_provider.py
        ├── sdxl_provider.py
        └── provider_registry.py
```

---

# Base Provider

Файл:

```text
providers/base.py
```

Назначение:

базовый контракт всех моделей.

---

# FLUX Provider

Файл:

```text
providers/flux_provider.py
```

Поддерживает:

* FLUX.1 Schnell;
* FLUX.1 Dev;
* FLUX.1 Dev NF4;
* FLUX GGUF.

---

# Конфигурация моделей

Модели описываются через YAML.

Пример:

```yaml
models:

  default:
    provider: flux


  flux:

    model:
      name: flux1-schnell

    vram:
      required: 10


  flux-dev-nf4:

    model:
      name: flux-dev-nf4

    vram:
      required: 8
```

---

# Выбор модели

Выбор происходит через конфигурацию.

Пример:

```yaml
generation:

  provider:
    flux


  model:
    flux-dev-nf4
```

---

# Возможности Provider

Каждый Provider должен сообщать:

```json
{
 "name": "flux-dev-nf4",
 "type": "diffusion",
 "max_resolution": "2048x2048",
 "supports_lora": true
}
```

---

# Поддержка разных клиентов

Provider не зависит от:

* MiMo Code;
* Claude Code;
* Gemini CLI.

Он работает только внутри Toolkit.

---

# Пример добавления новой модели

Добавление SDXL:

Создать:

```text
providers/

└── sdxl_provider.py
```

Добавить:

```yaml
models:

  sdxl:
    provider: sdxl
```

MCP Tools менять не требуется.

---

# Приоритеты выбора модели

При выборе модели учитывать:

1. доступную VRAM;
2. качество;
3. скорость;
4. назначение изображения.

Пример:

Hero:

```
FLUX.1 Dev
```

Быстрый preview:

```
FLUX.1 Schnell
```

---

# Работа с RTX 3080 10 GB

Рекомендуемые варианты:

## Быстрая генерация

FLUX.1 Schnell

---

## Максимальное качество

FLUX.1 Dev NF4/GGUF

---

## Ограничения

Одновременно используется:

```text
1 модель
1 generation job
```

---

# Будущее расширение

Архитектура допускает добавление:

* Stable Diffusion;
* SDXL;
* Stable Diffusion 3.5;
* Imagen;
* внешних API;
* пользовательских моделей.

---

# Цель

Создать универсальный слой моделей, позволяющий MiMo Web Toolkit развиваться независимо от конкретного генератора изображений.
