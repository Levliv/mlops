import json
import logging
from pathlib import Path

from clearml import Task
import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_model(filepath="models/model.jbl"):
    logger.info("Loading model...")
    model = joblib.load(filepath)
    return model


def load_scaler(filepath="models/scaler.jbl"):
    logger.info("Loading scaler...")
    scaler = joblib.load(filepath)
    return scaler


def load_data():
    logger.info("Loading data...")
    df = pd.read_csv("data/processed/wine_cleaned.csv")
    logger.info(f"Shape: {df.shape}")
    return df


def prepare_features(df):
    X = df.drop("quality", axis=1)
    y = df["quality"]
    return X, y


def scale_features(X, scaler):
    logger.info("Scaling features...")
    X_scaled = scaler.transform(X)
    return X_scaled


def make_predictions(model, X):
    logger.info("Making predictions...")
    y_pred = model.predict(X)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X)
    else:
        y_proba = None
    logger.info(f"Made {len(y_pred)} predictions")
    return y_pred, y_proba


def evaluate_predictions(y_true, y_pred):
    logger.info("Evaluating predictions...")
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="macro", zero_division=0)
    recall = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

    metrics = {
        "accuracy": float(accuracy),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "f1_macro": float(f1),
    }

    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"Precision (macro): {precision:.4f}")
    logger.info(f"Recall (macro): {recall:.4f}")
    logger.info(f"F1 (macro): {f1:.4f}")

    logger.info("Classification Report:")
    logger.info(classification_report(y_true, y_pred))

    cm = confusion_matrix(y_true, y_pred)
    logger.info("Confusion Matrix:")
    logger.info(cm)

    return metrics, cm


def save_metrics(metrics, filepath):
    logger.info("Saving metrics...")
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=4)


def save_predictions(y_pred, y_true, y_proba=None, filepath="metrics/predictions.csv"):
    logger.info("Saving predictions...")
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    pred_df = pd.DataFrame(
        {
            "true_quality": y_true.values,
            "predicted_quality": y_pred,
            "correct": (y_true.values == y_pred).astype(int),
        }
    )

    if y_proba is not None:
        classes = sorted(y_true.unique())
        for idx, quality_class in enumerate(classes):
            pred_df[f"prob_quality_{quality_class}"] = y_proba[:, idx]

    pred_df.to_csv(filepath, index=False)
    logger.info(f"Saved {len(pred_df)} predictions")


def save_confusion_matrix(cm, y_true, filepath):
    logger.info("Saving confusion matrix...")
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    classes = sorted(y_true.unique())
    df_cm = pd.DataFrame(
        cm, index=[f"true_{c}" for c in classes], columns=[f"pred_{c}" for c in classes]
    )
    df_cm.to_csv(filepath)


def main():
    logger.info("=" * 70)
    logger.info("Wine Quality Classification - Evaluation")
    logger.info("=" * 70)

    task = Task.init(project_name="wine-quality", task_name="model-evaluation")

    model = load_model("models/model.jbl")
    scaler = load_scaler("models/scaler.jbl")
    df = load_data()
    X, y = prepare_features(df)
    X_scaled = scale_features(X, scaler)
    y_pred, y_proba = make_predictions(model, X_scaled)
    metrics, cm = evaluate_predictions(y, y_pred)

    save_metrics(metrics, "metrics/eval_metrics.json")
    save_predictions(y_pred, y, y_proba, "metrics/predictions.csv")
    save_confusion_matrix(cm, y, "metrics/confusion_matrix.csv")

    task.get_logger().report_scalar("Accuracy", "evaluation", value=metrics["accuracy"], iteration=0)
    task.get_logger().report_scalar("F1 Score", "evaluation", value=metrics["f1_macro"], iteration=0)

    logger.info("=" * 70)
    logger.info("Evaluation completed!")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
