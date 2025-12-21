from datetime import datetime
import json
from pathlib import Path

import matplotlib.pyplot as plt
import yaml


def generate_experiment_report():
    """Генерирует отчет с графиками"""

    # Загрузи метрики
    with open("metrics/train_metrics.json") as f:
        metrics = json.load(f)

    # Загрузи конфигурацию
    with open("params.yaml") as f:
        config = yaml.safe_load(f)

    # Создай папку для изображений
    Path("docs/images").mkdir(parents=True, exist_ok=True)

    # График 1: Metrics comparison
    plt.figure(figsize=(10, 6))
    metric_names = ['Train\nAccuracy', 'Test\nAccuracy', 'Precision', 'Recall', 'F1 Score']
    metric_values = [
        metrics['train_accuracy'],
        metrics['test_accuracy'],
        metrics['test_precision_macro'],
        metrics['test_recall_macro'],
        metrics['test_f1_macro']
    ]
    colors = ['#2ecc71' if v > 0.7 else '#e74c3c' for v in metric_values]

    plt.bar(metric_names, metric_values, color=colors, alpha=0.7)
    plt.ylabel('Score', fontsize=12)
    plt.title('Model Performance Metrics', fontsize=14, fontweight='bold')
    plt.ylim(0, 1)
    plt.axhline(y=0.7, color='orange', linestyle='--', label='Target threshold')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('docs/images/current_metrics.png', dpi=300)
    plt.close()

    # Извлеки параметры модели
    train_config = config['train']['model']
    train_params = config['train']

    # Создай Markdown отчет
    report = f"""# Отчет об эксперименте

**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Результаты обучения

![Metrics](../images/current_metrics.png)

### Таблица метрик

| Метрика | Train | Test |
|---------|-------|------|
| Accuracy | {metrics['train_accuracy']:.4f} | {metrics['test_accuracy']:.4f} |
| Precision | - | {metrics['test_precision_macro']:.4f} |
| Recall | - | {metrics['test_recall_macro']:.4f} |
| F1 Score | - | {metrics['test_f1_macro']:.4f} |

## Конфигурация
```yaml
model_type: {train_config['model_type']}
n_estimators: {train_config['n_estimators']}
max_depth: {train_config['max_depth']}
min_samples_split: {train_config['min_samples_split']}
min_samples_leaf: {train_config['min_samples_leaf']}
random_state: {train_params['random_state']}
test_size: {train_params['test_size']}
```

## Выводы

### Качество модели

Модель показывает test accuracy **{metrics['test_accuracy']:.2%}**.

### Переобучение

Разница между train и test accuracy: **{metrics['train_accuracy'] - metrics['test_accuracy']:.2%}**
"""

    # Сохрани отчет
    Path("docs/experiments").mkdir(exist_ok=True, parents=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"docs/experiments/experiment_{timestamp}.md"

    with open(report_path, "w", encoding='utf-8') as f:
        f.write(report)

    # Также сохрани как latest
    with open("docs/experiments/latest.md", "w", encoding='utf-8') as f:
        f.write(report)

    print(f"Report saved to {report_path}")
    print("Latest report: docs/experiments/latest.md")
