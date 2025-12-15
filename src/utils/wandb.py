"""Утилиты для W&B логирования экспериментов"""

from functools import wraps
import logging
from typing import Any, Callable, Dict, Optional, Tuple

import wandb

logger = logging.getLogger(__name__)


def track_experiment(
    project: str = "wine-quality",
    tags: Optional[list] = None,
    log_confusion_matrix: bool = False,
) -> Callable:
    """
    Декоратор для отслеживания экспериментов в W&B.

    Автоматически:
    - Инициализирует W&B run
    - Логирует параметры конфига
    - Логирует метрики из словаря результатов
    - Завершает run

    Args:
        project: Название проекта W&B
        tags: Теги для эксперимента
        log_confusion_matrix: Логировать ли матрицу ошибок

    Returns:
        Декоратор функции
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            config: Dict[str, Any], *args: Any, **kwargs: Any
        ) -> Tuple[Dict[str, float], Any, Any]:
            # Подготовить данные для W&B
            model_type = config.get("train", {}).get("model_type", "Unknown")
            n_estimators = config.get("train", {}).get("n_estimators", 100)
            max_depth = config.get("train", {}).get("max_depth", 10)

            run_name = f"{model_type}_e{n_estimators}_d{max_depth}"

            # Инициализировать W&B
            run = wandb.init(  # type: ignore[attr-defined]
                project=project,
                name=run_name,
                config=config.get("train", {}),
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
