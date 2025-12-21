from datetime import datetime

from clearml import Task
import pandas as pd


def compare_experiments():
    """Сравнивает все эксперименты"""

    # Получи все Tasks проекта wine-quality
    tasks = Task.get_tasks(
        project_name="wine-quality",
        task_name="training-experiment",
        task_filter={'status': ['completed', 'stopped']}  # Только завершенные
    )

    print(f"Found {len(tasks)} tasks")

    # Собери данные
    data = []
    for task in tasks[:10]:  # Последние 10
        print(f"Processing task {task.id[:8]}...")

        # Получи параметры
        params = task.get_parameters()

        # Получи метрики из последних логов
        scalars = task.get_last_scalar_metrics()

        # Извлеки значения (исправленный способ!)
        test_acc = 0
        test_f1 = 0

        # ClearML возвращает словарь вида: {'title': {'series': {'last': value}}}
        for title, series_dict in scalars.items():
            if 'Accuracy' in title:
                for series, metrics in series_dict.items():
                    if 'test' in series:
                        test_acc = metrics.get('last', 0)
            if 'F1' in title:
                for series, metrics in series_dict.items():
                    if 'test' in series:
                        test_f1 = metrics.get('last', 0)

        # Если метрик нет в scalars, попробуй из artifacts
        if test_acc == 0:
            artifacts = task.artifacts
            for artifact_name, artifact_obj in artifacts.items():
                if 'metrics' in artifact_name.lower():
                    metrics_data = artifact_obj.get()
                    if isinstance(metrics_data, dict):
                        test_acc = metrics_data.get('test_accuracy', 0)
                        test_f1 = metrics_data.get('test_f1_macro', 0)

        data.append({
            "ID": task.id[:8],
            "Date": task.data.started.strftime('%Y-%m-%d %H:%M') if task.data.started else "N/A",
            "Model": params.get('General/model_type', params.get('model_type', 'N/A')),
            "N Estimators": params.get('General/n_estimators', params.get('n_estimators', 'N/A')),
            "Max Depth": params.get('General/max_depth', params.get('max_depth', 'N/A')),
            "Accuracy": round(test_acc, 4),
            "F1": round(test_f1, 4)
        })

    # Создай DataFrame
    df = pd.DataFrame(data)

    # Отсортируй по Accuracy
    df = df.sort_values('Accuracy', ascending=False)

    # Создай Markdown таблицу
    markdown_table = df.to_markdown(index=False)

    # Найди лучший эксперимент
    best_idx = df['Accuracy'].idxmax()
    best_id = df.loc[best_idx, 'ID']
    best_acc = df.loc[best_idx, 'Accuracy']

    report = f"""# Сравнение экспериментов

**Дата генерации:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Все эксперименты

{markdown_table}

## Лучший эксперимент

- **ID:** {best_id}
- **Accuracy:** {best_acc:.4f}
- **Model:** {df.loc[best_idx, 'Model']}
- **N Estimators:** {df.loc[best_idx, 'N Estimators']}
- **Max Depth:** {df.loc[best_idx, 'Max Depth']}

## Статистика

- Всего экспериментов: {len(df)}
- Средняя точность: {df['Accuracy'].mean():.4f}
- Лучшая точность: {df['Accuracy'].max():.4f}
- Худшая точность: {df['Accuracy'].min():.4f}
"""

    # Сохрани отчет
    from pathlib import Path
    Path("docs/experiments").mkdir(parents=True, exist_ok=True)

    with open("docs/experiments/comparison.md", "w", encoding='utf-8') as f:
        f.write(report)

    print("Comparison saved to docs/experiments/comparison.md")
    print(f"Preview:\n{report}")
