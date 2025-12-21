# Обучение модели

## Запуск обучения
```bash
poetry run python src/modeling/train.py
```

## Параметры

Настрой в `params.yaml`:
```yaml
train:
  model:
    model_type: RandomForest
    n_estimators: 40
    max_depth: 10
```

## Результаты

- Модель: `models/model.jbl`
- Метрики: `metrics/train_metrics.json`
