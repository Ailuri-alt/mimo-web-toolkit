# COMFYUI_SETUP.md

# ComfyUI Setup Guide

## MiMo Web Toolkit

Версия: 1.0

---

# Назначение

Этот документ описывает настройку ComfyUI для работы совместно с **MiMo Web Toolkit**.

Целевая система:

* Windows 10;
* NVIDIA RTX 3080;
* 10 GB VRAM;
* 32 GB RAM;
* локальный запуск;
* управление через MCP Toolkit.

---

# Роль ComfyUI в системе

ComfyUI является движком генерации изображений.

Архитектура:

```text
MiMo Code

    |
    |
    v

MCP Server

    |
    |
    v

MiMo Web Toolkit

    |
    |
    v

ComfyUI API

    |
    |
    v

AI Model
```

ComfyUI не должен знать о существовании MiMo Code.

---

# Требования

## Аппаратные требования

Минимальная рекомендуемая конфигурация:

* NVIDIA GPU;
* CUDA поддержка;
* 10 GB VRAM;
* 32 GB RAM.

---

# Установка ComfyUI

Рекомендуемый вариант:

```text
ComfyUI Portable
```

или

```text
Git installation
```

---

# Рекомендуемая структура

```text
ComfyUI/

├── main.py
├── models/
│
├── custom_nodes/
│
├── output/
│
└── workflows/
```

---

# Установка моделей

Модели должны храниться отдельно от Toolkit.

Пример:

```text
ComfyUI/

models/

├── checkpoints/
│
├── diffusion_models/
│
├── text_encoders/
│
├── vae/
│
└── loras/
```

---

# FLUX.1 Schnell

Пример размещения:

```text
models/

diffusion_models/

└── flux1-schnell.safetensors


text_encoders/

├── clip_l.safetensors
└── t5xxl_fp8.safetensors


vae/

└── ae.safetensors
```

---

# FLUX.1 Dev NF4 / GGUF

Для RTX 3080 10 GB рекомендуется использовать оптимизированные варианты.

Например:

```text
models/

diffusion_models/

├── flux-dev-nf4
└── flux-dev-gguf
```

Преимущества:

* меньше VRAM;
* быстрее загрузка;
* стабильнее работа.

---

# Запуск ComfyUI

Для RTX 3080 рекомендуется:

```bat
python main.py ^
 --lowvram ^
 --cuda-malloc ^
 --listen 127.0.0.1 ^
 --port 8188
```

---

# Пояснение параметров

## --lowvram

Использование оптимизации памяти.

Необходимо для GPU с 10 GB VRAM.

---

## --cuda-malloc

Оптимизация распределения памяти CUDA.

---

## --listen

Ограничивает доступ локальным компьютером.

---

## --port

Стандартный порт API.

```text
8188
```

---

# Настройки для MiMo Web Toolkit

В:

```text
config/settings.yaml
```

будет:

```yaml
comfyui:

  host:
    127.0.0.1

  port:
    8188

  timeout:
    600
```

---

# Ограничения RTX 3080

Для стабильной работы:

```yaml
generation:

  max_parallel_jobs: 1

  batch_size: 1
```

---

# Workflow

Toolkit не генерирует workflow программно.

Workflow хранятся отдельно:

```text
workflows/

└── flux/

    ├── hero.json
    ├── product.json
    ├── portrait.json
    └── background.json
```

---

# Требования к Workflow

Каждый workflow должен:

* быть протестирован вручную;
* работать через API;
* иметь понятное имя;
* использовать поддерживаемую модель.

---

# API режим

ComfyUI должен быть доступен через:

```text
http://127.0.0.1:8188
```

Toolkit использует:

* отправку workflow;
* получение ID задачи;
* отслеживание выполнения;
* получение результата.

---

# Очередь генерации

Так как FLUX является ресурсоёмкой моделью:

одновременно выполняется:

```text
1 generation job
```

Очередь управляется:

```text
queue_manager.py
```

---

# Оптимизация памяти

Рекомендуется:

* закрывать лишние AI-приложения;
* не запускать несколько ComfyUI;
* использовать одну модель одновременно;
* применять FP8/NF4/GGUF варианты.

---

# Проверка установки

Перед подключением Toolkit необходимо проверить:

1. ComfyUI запускается.
2. Workflow выполняется вручную.
3. Изображение появляется в output.
4. API доступен.

---

# Интеграция с Toolkit

После успешной настройки:

```
ComfyUI
    |
    |
MiMo Web Toolkit
    |
    |
MiMo Code
```

становятся единой системой генерации изображений.

---

# Цель

Получить стабильный локальный AI image backend, оптимизированный под ограничение RTX 3080 10 GB и управляемый через MCP.
