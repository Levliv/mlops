from typing import List, Literal, Union

from pydantic import BaseModel, Field


class PrepareConfig(BaseModel):
    input_file: str
    output_file: str


# Базовая конфигурация (общие параметры)
class BaseModelConfig(BaseModel):
    random_state: int = Field(default=42)
    test_size: float = Field(gt=0, lt=1, default=0.2)


# Конфигурация для RandomForest
class RandomForestConfig(BaseModelConfig):
    model_type: Literal["RandomForest"] = "RandomForest"
    n_estimators: int = Field(gt=0, default=100)
    max_depth: int = Field(gt=0, default=10)
    min_samples_split: int = Field(ge=2, default=5)
    min_samples_leaf: int = Field(ge=1, default=2)


# Конфигурация для GradientBoosting
class GradientBoostingConfig(BaseModelConfig):
    model_type: Literal["GradientBoosting"] = "GradientBoosting"
    n_estimators: int = Field(gt=0, default=100)
    max_depth: int = Field(gt=0, default=5)
    learning_rate: float = Field(gt=0, lt=1, default=0.1)


# Общая конфигурация обучения
class TrainConfig(BaseModel):
    model: Union[RandomForestConfig, GradientBoostingConfig]


class EvaluateConfig(BaseModel):
    metrics: List[str]


class Config(BaseModel):
    prepare: PrepareConfig
    train: TrainConfig
    evaluate: EvaluateConfig
