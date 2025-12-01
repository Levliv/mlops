# wine_quality

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

project to asses wine quality

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
### Отчет о настройке рабочего места Data Scientist (ДЗ1)
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
- Настроен Git репозиторий, создан .gitignore для ML проекта (исключены venv, pycache, модели, raw data).
- Стратегия ветвления: Feature Branch Workflow
    - `master` Основная ветка. Содержит только стабильный, протестированный код.
    - `feature/hwN` Ветки для выполнения домашних заданий. Отделяются от master. После выполнения задания и прохождения тестов, проверки вливается в master
    - `fix/<name>`: Ветки для исправления багов. Отделяются от master. После выполнения задания и прохождения тестов, вливается в master без review.
#### 5. Отчет о проделанной работе
