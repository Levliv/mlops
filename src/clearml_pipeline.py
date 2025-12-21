from clearml import PipelineController

pipe = PipelineController(
    name="wine-quality-pipeline",
    project="wine-quality"
)

# ДОБАВЬ ЭТУ СТРОКУ:
pipe.set_default_execution_queue("default")

# Этап 1: Подготовка данных
pipe.add_step(
    name="data_preparation",
    base_task_project="wine-quality",
    base_task_name="data-preparation"
)

# Этап 2: Обучение модели
pipe.add_step(
    name="train_model",
    parents=["data_preparation"],
    base_task_project="wine-quality",
    base_task_name="training-experiment"
)

# Этап 3: Оценка модели
pipe.add_step(
    name="evaluate_model",
    parents=["train_model"],
    base_task_project="wine-quality",
    base_task_name="model-evaluation"
)

pipe.start_locally(run_pipeline_steps_locally=True)
print("Pipeline started!")
