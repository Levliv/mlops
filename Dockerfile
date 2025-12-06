# Используем Python образ
FROM python:3.12-slim


# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установим рабочую папку
WORKDIR /app

# Зависимостей
RUN pip install poetry

# Копируем весь проект
COPY . .

COPY pyproject.toml poetry.lock ./

# Установим Python зависимости
RUN poetry config virtualenvs.create false && \
    poetry install

RUN git init && \
    git config user.email "docker@example.com" && \
    git config user.name "Docker"

RUN dvc pull

# Открытие порта для Jupyter
EXPOSE 8888

# Команда по умолчанию - запуск Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
