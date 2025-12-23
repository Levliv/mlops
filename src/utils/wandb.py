"""Утилиты для W&B логирования экспериментов"""

from functools import wraps
import logging
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

from src.config.schemas import Config
import wandb

logger = logging.getLogger(__name__)


def track_experiment(
    project: str = "wine-quality",
    tags: Optional[list] = None,
) -> Callable:
    """
    Декоратор для отслеживания экспериментов в W&B.

    Автоматически:
    - Инициализирует W&B run
    - Логирует параметры конфига
    - Логирует метрики
    - Логирует модель как артефакт
    - Отправляет уведомления о результатах
    - Завершает run

    Args:
        project: Название проекта W&B
        tags: Теги для эксперимента

    Returns:
        Декоратор функции
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            config: Config, *args: Any, **kwargs: Any
        ) -> Tuple[dict[str, float], Any, Any]:
            # Подготовить данные для W&B из Pydantic модели
            model_type = config.train.model.model_type
            n_estimators = config.train.model.n_estimators
            max_depth = config.train.model.max_depth

            run_name = f"{model_type}_e{n_estimators}_d{max_depth}"

            # Инициализировать W&B
            run = wandb.init(  # type: ignore[attr-defined]
                project=project,
                name=run_name,
                config=config.train.model.model_dump(),
                tags=tags or [model_type, "classification"],
            )

            try:
                # Уведомление о старте
                logger.info(f"🚀 Training started: {run_name}")

                # Запустить функцию
                result = func(config, *args, **kwargs)

                # Результат должен быть кортежем (metrics, y_test_pred, y_test)
                if isinstance(result, tuple) and len(result) == 3:
                    metrics, y_test_pred, y_test = result

                    # Логировать метрики
                    wandb.log(metrics)  # type: ignore[attr-defined]
                    logger.info(f"Logged metrics: {list(metrics.keys())}")

                    # Логировать модель
                    _log_model(run_name)

                    # Отправить уведомление о результатах
                    _send_success_notification(metrics, config)

                return result

            except Exception as e:
                logger.error(f"❌ Error in experiment: {e}")
                wandb.log({"error": str(e)})  # type: ignore[attr-defined]

                # Отправить уведомление об ошибке
                _send_failure_notification(e, config)

                raise
            finally:
                run.finish()
                logger.info(f"Finished W&B run: {run_name}")

        return wrapper

    return decorator


def _send_success_notification(metrics: dict, config: Config) -> None:
    """Отправляет уведомление об успешном обучении"""
    test_accuracy = metrics.get('test_accuracy', 0)
    test_f1 = metrics.get('test_f1_macro', 0)

    # Уведомление если точность низкая
    if test_accuracy < 0.7:
        wandb.alert(  # type: ignore[attr-defined]
            title="⚠️ Low Accuracy Warning",
            text=f"Model: {config.train.model.model_type}\n"
                 f"Test Accuracy: {test_accuracy:.2%}\n"
                 f"F1 Score: {test_f1:.2%}\n"
                 f"Consider tuning hyperparameters!",
            level=wandb.AlertLevel.WARN  # type: ignore[attr-defined]
        )
        logger.warning(f"⚠️ Low accuracy: {test_accuracy:.2%}")
    else:
        # Уведомление об успехе
        wandb.alert(  # type: ignore[attr-defined]
            title="✅ Training Completed Successfully",
            text=f"Model: {config.train.model.model_type}\n"
                 f"Test Accuracy: {test_accuracy:.2%}\n"
                 f"F1 Score: {test_f1:.2%}\n"
                 f"All metrics look good!",
            level=wandb.AlertLevel.INFO  # type: ignore[attr-defined]
        )
        logger.info(f"✅ Training successful: {test_accuracy:.2%}")


def _send_failure_notification(error: Exception, config: Config) -> None:
    """Отправляет уведомление об ошибке"""
    wandb.alert(  # type: ignore[attr-defined]
        title="❌ Training Failed",
        text=f"Model: {config.train.model.model_type}\n"
             f"Error: {str(error)}\n"
             f"Check logs for details.",
        level=wandb.AlertLevel.ERROR  # type: ignore[attr-defined]
    )
    logger.error(f"❌ Training failed: {error}")


def _log_model(run_name: str) -> None:
    """Логирует модель как артефакт (вспомогательная функция)"""
    model_path = Path("models/model.jbl")

    if not model_path.exists():
        logger.warning(f"Model not found: {model_path}")
        return

    try:
        artifact = wandb.Artifact(  # type: ignore[attr-defined]
            name="wine-quality-model",
            type="model",
            description=f"Model: {run_name}",
        )
        artifact.add_file(str(model_path), name="model.jbl")
        wandb.log_artifact(artifact)  # type: ignore[attr-defined]
        logger.info(f"Model logged: {model_path}")
    except Exception as e:
        logger.error(f"Failed to log model: {e}")
