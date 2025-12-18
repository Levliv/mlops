# wine_quality

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

project to asses wine quality

# Table of contents
- [1. Project Organization](#Project-Organization)
- [2. How to run](#How-to-run)
- [3. Отчеты]()
  - [3.1 ДЗ 1](#ДЗ1)
  - [3.2 ДЗ 2](#ДЗ2)
  - [3.3 ДЗ 3](#ДЗ3)
  - [3.4 ДЗ 4](#ДЗ4)
- [4. Примеры](#примеры)
## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         src and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling
    │   ├── __init__.py
    │   ├── predict.py          <- Code to run model inference with trained models
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```
--------
## How to run
1. Клонируйте репозиторий
```
git clone https://github.com/Levliv/mlops.git
cd mlops/wine_quality
```
2. Соберите Docker образ
```
docker build -t wine-quality .
```
3. Запустите контейнер
```
docker run -p 8888:8888 wine-quality
```
Вы прекрасны: Откройте ссылку в браузере (будет выведена в терминале)


--------
## ДЗ1
### Отчет о настройке рабочего места Data Scientist
#### 1. Структура проекта:
Использован [Cookiecutter DS](https://cookiecutter-data-science.drivendata.org/)
```
pip install cookiecutter-data-science
ccds
```
- Создан подробный README.md, включающий:
- Описание проекта
- Структура проекта
- Инструкция по установке
- Руководство по использованию
- Описание инструментов качества кода

#### 2.Качество кода :
- Настроены pre-commit hooks: Black, isort, Ruff, MyPy, Bandit
- Настроено форматирование кода (Black, isort, Ruff)
- Настроены линтеры (Ruff, MyPy, Bandit)
- Созданы конфигурационные файлы
![pre-commit hooks](img/hw1/pre_commit_hooks.png)

#### 3.Управление зависимостями:
- Настрено управлнеие зависимостями с Poetry
- Создан requirements.txt с точными версиями
- Настроено виртуальное окружение c Poetry
![pre-commit hooks](img/hw1/poetry_env.png)
- Создан Dockerfile для контейнеризации
![Docker](img/hw1/docker_run.png)

#### 4.Git workflow :
- Настроиен Git репозиторий
- Создан .gitignore для ML проекта
- Настроены ветки для разных этапов работы

#### 5. Отчет о проделанной работе


--------
## ДЗ2
### Отчет о настройке dерсионирование данных и моделей
#### 1. Настройка DVC для версионирования даных:
- Установлен и инициализирован DVC
```
poetry add dvc
poetry install
dvc init
```
- Настроен remote storage (Local)
```
mkdir -p storage/local/dvc-storage
dvc remote add -d local storage/local/dvc-storage
dvc add .
dvc push
```
- Создана система версионирования данных
- Настроено автоматическое создание версий
![dvc_data](img/hw2/dvc_data.png)

#### 2. Настройка DVC для версионирования моделей:
- Настроен dvc для версионирования моделей
- Настроена система версионирования метаданных для моделей
- Настроено сохранение метаданных для моделей
- Создана система сравнения версий
![dvc_models](img/hw2/dvc_model.png)

#### 3.Воспроизводимость:
- Инструкция по воспроизведению: добавлены в соответствующие пункты отчета
- Настроены версеии зависимостей: poetry
- Протестировано решение
- Создан Docker контейнер
![Docker-compose](img/hw2/docker-compose.png)

#### 4. Отчет о проделанной работе


--------
## ДЗ3
### Отчет о настройке трекинга экспериментов
#### 1. Настройка выбранного инструмента: Weights & Biases
- Установлен и инициализирован Weights & Biases
- Настроиено облачное хранилище
- создан проект и эксперименты
- Настроена аутентификация с API_KEY
```
poetry add wandb
poetry install
wandb login
<enter API key recieved https://wandb.ai>
```

#### 2. Проведение экспериментов:
- Проведено 15+ экспериментов с разными алгоритмами sweepe
  - создан файл sweep.yaml с сеткой гиперпараметров для оптимизации
  - создана серия экспериментов ```wandb sweep sweep.yaml```
  - Проведена серия экспериментов ```wandb agent livshitz-leva-itmo-university/wine-quality/7cn398y4 --count 15```
- Настроено логирование метрик, параметров и артефактов
- Создано система сравнения экспериментов
- Настроена фильтрация и поиск экспериментов
![model runs](img/hw3/model_runs.png)

#### 3.Интеграция с кодом:
- Интегрирован выбранный инструмент в Python код
- Созданы декораторы для автоматического логирования: [декоратор](src/utils/wandb.py)
- Настроены [контекстные менеджеры](src/utils/wandb.py)
- Cозданы [утилиты для работы с экспериментами](src/utils/wandb.py)
![Docker-compose](img/hw3/model_registery.png)

#### 4. Отчет о проделанной работе


--------
## ДЗ4
### Отчет о Автоматизация ML пайплайнов
#### 1. Настройка выбранного инструмента оркестрации: DVC Pipelines
- Установлен и настроен DVC Pipelines (см. ДЗ 2 и 3)
- Создан workflow для ML пайплайна: [dvc.yaml](dvc.yaml)
- Настроена зависимости между этапами: ![dvc dag](img/hw4/dvc_dag.png)
- Реализовано кэширование и параллельное выполнение: DVC автоматически кэширует результаты каждого этапа ![dvc repro](img/hw4/dvc_repro.png)

#### 2. Настройка выбранного инструмента конфигураций: Pydantic
- Установлен и настроен Pydantic
- Созданы конфигурации для разных алгоритмов
- Настроена валидацию конфигураций
- Создана систему композиции конфигураций
![model runs](img/hw4/???)

#### 3.Интеграция и тестирование :
- Интегрирован выбранный инструмент в Python код
- Создана система мониторинга выполнения
- Настроены уведомления о результатах
- Протестирована воспроизводимость
![Docker-compose](img/hw4/???)

#### 4. Отчет о проделанной работе
