from datetime import datetime
import json

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

# Загрузить данные
df = pd.read_csv("data/processed/wine_cleaned.csv")
X = df.drop("quality", axis=1)
y = df["quality"]

# Разделить данные
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучить модель
n_estimators = 100
max_depth = 10
model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
model.fit(X_train, y_train)
print("Модель обучена")

# Предсказания
y_pred = model.predict(X_test)

# Метрики
metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, average="weighted"),
    "recall": recall_score(y_test, y_pred, average="weighted"),
    "f1": f1_score(y_test, y_pred, average="weighted"),
}

print(f"Метрики: {metrics}")

# Сохранить модель
joblib.dump(model, "models/model_v1.joblib")

model_metadata = {
    "model_name": "RandomForest",
    "version": "1.0",
    "metrics": metrics,
    "hyperparameters": {"n_estimators": n_estimators, "max_depth": max_depth},
    "training_samples": len(X_train),
    "timestamp": datetime.now().isoformat(),
}

with open("models/model_v1_metadata.json", "w") as f:
    json.dump(model_metadata, f, indent=2)

print("Модель сохранена в models/model_v1.joblib")
