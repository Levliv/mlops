import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def prepare_data():
    """Подготовка данных согласно DVC pipeline"""
    logger.info("Loading raw data...")
    df_raw = pd.read_csv("data/raw/wineQT.csv")
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

    logger.info("Saving processed data...")
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df_processed.to_csv("data/processed/wine_cleaned.csv", index=False)

    logger.info(
        f"Done! Samples: {len(df_processed)}, Features: {len(df_processed.columns) - 1}, Classes: {df_processed['quality'].nunique()}"
    )

    return df_processed


if __name__ == "__main__":
    prepare_data()
