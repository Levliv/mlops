# Используем Python образ
FROM python:3.12-slim


# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установим рабочую папку
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Установим Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открытие порта для Jupyter
EXPOSE 8888

# Команда по умолчанию - запуск Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
