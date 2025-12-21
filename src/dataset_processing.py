import logging
from pathlib import Path

from clearml import Task
import pandas as pd
import yaml

from src.config.schemas import Config

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_config():
    """Загрузка конфигурации с валидацией"""
    with open("params.yaml") as f:
        data = yaml.safe_load(f)
    return Config(**data)


def prepare_data():
    """Подготовка данных согласно DVC pipeline"""
    Task.init(project_name="wine-quality", task_name="data-preparation")

    # Загружаем конфиг
    config = load_config()

    # Используем пути из конфига
    input_file = config.prepare.input_file
    output_file = config.prepare.output_file

    logger.info(f"Loading raw data from {input_file}...")
    df_raw = pd.read_csv(input_file)
    logger.info(f"Initial size: {len(df_raw)} rows, {len(df_raw.columns)} columns")
    logger.info(f"Columns: {list(df_raw.columns)}")

    logger.info("Processing data...")

    if "Id" in df_raw.columns:
        df_processed = df_raw.drop("Id", axis=1)
        logger.info("Removed 'Id' column")
    else:
        df_processed = df_raw.copy()

    initial_len = len(df_processed)
    df_processed = df_processed.drop_duplicates()
    logger.info(
        f"After removing duplicates: {len(df_processed)} rows (removed {initial_len - len(df_processed)})"
    )

    initial_len = len(df_processed)
    df_processed = df_processed.dropna()
    logger.info(
        f"After removing NaN: {len(df_processed)} rows (removed {initial_len - len(df_processed)})"
    )

    logger.info("Quality distribution:")
    logger.info(df_processed["quality"].value_counts().sort_index())
    logger.info(
        f"Min: {df_processed['quality'].min()}, Max: {df_processed['quality'].max()}, Mean: {df_processed['quality'].mean():.2f}"
    )

    logger.info(f"Saving processed data to {output_file}...")
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df_processed.to_csv(output_file, index=False)

    logger.info(
        f"Done! Samples: {len(df_processed)}, Features: {len(df_processed.columns) - 1}, Classes: {df_processed['quality'].nunique()}"
    )

    return df_processed


if __name__ == "__main__":
    prepare_data()
