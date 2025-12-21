from clearml.automation import TaskScheduler

# Создай планировщик
scheduler = TaskScheduler()

# Настрой расписание - каждый день в 2:00
scheduler.add_task(
    schedule_task_id="c46c709ccd3d4182861f348972885a59",
    queue="default",
    name="wine-quality-daily-training",
    target_project="wine-quality",
    hour=2,      # Оба параметра обязательны!
    minute=0     # Оба параметра обязательны!
)

# Запусти планировщик
scheduler.start()
print("Scheduler started! Pipeline will run daily at 02:00")
