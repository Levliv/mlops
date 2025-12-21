# Установка и развертывание

## Требования

- Python 3.12+
- Poetry
- Docker (для ClearML)

## Установка

### 1. Клонируй репозиторий
```bash
git clone https://github.com/Levliv/mlops.git
cd mlops
```

### 2. Установи зависимости
```bash
poetry install
```

### 3. Настрой DVC
```bash
dvc pull
```

### 4. Запусти ClearML Server
```bash
cd clearml-server/docker
docker-compose up -d
```

### 5. Инициализируй ClearML
```bash
poetry run clearml-init
```
