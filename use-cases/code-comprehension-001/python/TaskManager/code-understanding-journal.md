Task Manager Code Understanding Journal

Part 1 — Task Creation & Status Updates
Files Involved: cli.py, TaskManager, storage.py, models.py
Flow of Task Creation:
CLI → TaskManager.create_task() → Task object → TaskStorage.add_task() → tasks.json

Status Update (DONE):
CLI → TaskManager.update_task_status() → task.mark_as_done() → storage.save()

... (rest of your journal content) ...
