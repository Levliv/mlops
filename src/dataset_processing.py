# src/dataset.py
import pandas as pd

# 1. Загрузить raw данные
df_raw = pd.read_csv("data/raw/wineQT.csv")

# 2. Обработать
df_processed = df_raw.drop_duplicates()
df_processed = df_processed.dropna()

# 3. Сохранить processed
df_processed.to_csv("data/processed/wine_cleaned.csv", index=False)
