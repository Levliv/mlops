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
            config: Config, *args: Any, **kwargs: Any  # ← Тип изменен на Config
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
                config=config.train.model.model_dump(),  # ← Используем model_dump()
                tags=tags or [model_type, "classification"],
            )

            try:
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

                return result

            except Exception as e:
                logger.error(f"Error in experiment: {e}")
                wandb.log({"error": str(e)})  # type: ignore[attr-defined]
                raise
            finally:
                run.finish()
                logger.info(f"Finished W&B run: {run_name}")

        return wrapper

    return decorator


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
