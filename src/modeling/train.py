import json
import logging
from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import yaml

from src.utils.wandb import track_experiment

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_params():
    with open("params.yaml") as f:
        return yaml.safe_load(f)


def load_data():
    logger.info("Loading data...")
    df = pd.read_csv("data/processed/wine_cleaned.csv")
    logger.info(f"Shape: {df.shape}")
    return df


def prepare_features(df):
    logger.info("Preparing features...")
    X = df.drop("quality", axis=1)
    y = df["quality"]

    unique_classes = sorted(y.unique())
    logger.info(f"Features: {X.shape[1]}, Samples: {X.shape[0]}")
    logger.info(f"Classes: {len(unique_classes)} -> {unique_classes}")
    logger.info("Quality distribution:")
    for quality in sorted(y.unique()):
        count = (y == quality).sum()
        pct = count / len(y) * 100
        logger.info(f"Quality {quality}: {count:4d} ({pct:5.1f}%)")

    return X, y


def split_data(X, y, params):
    logger.info("Splitting data...")
    test_size = params["train"].get("test_size", 0.2)
    random_state = params["train"].get("random_state", 42)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logger.info(f"Train: {len(X_train)} samples ({100 - int(test_size * 100)}%)")
    logger.info(f"Test: {len(X_test)} samples ({int(test_size * 100)}%)")

    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test):
    logger.info("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def train_model(X_train, y_train, params):
    logger.info("Training model...")
    train_params = params["train"]
    model_type = train_params.get("model_type", "RandomForest")

    if model_type == "RandomForest":
        model = RandomForestClassifier(
            n_estimators=train_params.get("n_estimators", 100),
            max_depth=train_params.get("max_depth", 10),
            min_samples_split=train_params.get("min_samples_split", 5),
            min_samples_leaf=train_params.get("min_samples_leaf", 2),
            random_state=train_params.get("random_state", 42),
            n_jobs=-1,
            verbose=0,
        )
    elif model_type == "GradientBoosting":
        model = GradientBoostingClassifier(
            n_estimators=train_params.get("n_estimators", 100),
            learning_rate=train_params.get("learning_rate", 0.1),
            max_depth=train_params.get("max_depth", 5),
            random_state=train_params.get("random_state", 42),
            verbose=0,
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    model.fit(X_train, y_train)
    logger.info(f"Model {model_type} trained")

    return model


def evaluate_model(model, X_train, X_test, y_train, y_test):
    logger.info("Evaluating model...")
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred, average="macro", zero_division=0)
    test_recall = recall_score(y_test, y_test_pred, average="macro", zero_division=0)
    test_f1 = f1_score(y_test, y_test_pred, average="macro", zero_division=0)

    metrics = {
        "train_accuracy": float(train_acc),
        "test_accuracy": float(test_acc),
        "test_precision_macro": float(test_precision),
        "test_recall_macro": float(test_recall),
        "test_f1_macro": float(test_f1),
    }

    logger.info(f"Train Accuracy: {train_acc:.4f}")
    logger.info(f"Test Accuracy: {test_acc:.4f}")
    logger.info(f"Test Precision (macro): {test_precision:.4f}")
    logger.info(f"Test Recall (macro): {test_recall:.4f}")
    logger.info(f"Test F1 (macro): {test_f1:.4f}")

    logger.info("Classification Report (Test Set):")
    logger.info(classification_report(y_test, y_test_pred))

    return metrics, y_test_pred, y_test


def save_model(model, filepath):
    logger.info("Saving model...")
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath, protocol=4)


def save_scaler(scaler, filepath):
    logger.info("Saving scaler...")
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, filepath, protocol=4)


def save_metrics(metrics, filepath):
    logger.info("Saving metrics...")
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=4)


@track_experiment(project="wine-quality", tags=["dvc-pipeline"])
def train_and_evaluate(params):
    """Обучение и оценка модели с логированием в W&B"""
    df = load_data()
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y, params)
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    save_scaler(scaler, "models/scaler.jbl")

    model = train_model(X_train_scaled, y_train, params)
    metrics, y_test_pred, y_test_result = evaluate_model(
        model, X_train_scaled, X_test_scaled, y_train, y_test
    )

    save_model(model, "models/model.jbl")
    save_metrics(metrics, "metrics/train_metrics.json")

    return metrics, y_test_pred, y_test_result


def main():
    logger.info("=" * 70)
    logger.info("Wine Quality Classification - Training")
    logger.info("=" * 70)

    params = load_params()
    train_and_evaluate(params)

    logger.info("=" * 70)
    logger.info("Training completed!")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
