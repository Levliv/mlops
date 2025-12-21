# Отчет об эксперименте

**Дата:** 2025-12-21 21:50:25

## Результаты обучения

![Metrics](../images/current_metrics.png)

### Таблица метрик

| Метрика | Train | Test |
|---------|-------|------|
| Accuracy | 0.8636 | 0.5735 |
| Precision | - | 0.2816 |
| Recall | - | 0.2752 |
| F1 Score | - | 0.2755 |

## Конфигурация
```yaml
model_type: RandomForest
n_estimators: 40
max_depth: 10
min_samples_split: 5
min_samples_leaf: 3
random_state: 42
test_size: 0.2
```

## Выводы

### Качество модели

Модель показывает test accuracy **57.35%**.

### Переобучение

Разница между train и test accuracy: **29.01%**
