# Быстрый старт

## Установка
````bash
git clone https://github.com/username/wine-quality.git
cd wine-quality
poetry install
````

## Запуск обучения
````bash
dvc repro
````

## Просмотр результатов

- ClearML: http://localhost:8080
- W&B: https://wandb.ai/your-project
````
````

`docs/guides/installation.md`:
````markdown
# Установка и развертывание

## Требования

- Python 3.12+
- Poetry
- Docker (для ClearML)

## Шаги установки

### 1. Клонируй репозиторий
```bash
git clone https://github.com/username/wine-quality.git
cd wine-quality
```

### 2. Установи зависимости
```bash
poetry install
```

### 3. Настрой DVC
```bash
dvc pull  # Скачать данные
```

### 4. Запусти ClearML Server
```bash
cd clearml-server/docker
docker-compose up -d
```

### 5. Настрой credentials
```bash
clearml-init
wandb login
```
````

**Шаг 5: Автогенерация документации из кода**

`docs/api/modules.md`:
````markdown
# API Reference

## Dataset Processing

::: src.utils.dataset_processing
    options:
      show_root_heading: true
      show_source: true

## Training

::: src.modeling.train
    options:
      show_root_heading: true
````
