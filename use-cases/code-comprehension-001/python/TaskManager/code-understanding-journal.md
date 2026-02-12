what if i do it like this > tests/test_task_parser.py << 'EOF'                                                   Task Manager Code Understanding Journal

Part 1 — Task Creation & Status Updates

Files Involved: cli.py, TaskManager, storage.py, models.py
Flow of Task Creation:

CLI → TaskManager.create_task() → Task object → TaskStorage.add_task() → tasks.json


Status Update (DONE):

CLI → TaskManager.update_task_status() → task.mark_as_done() → storage.save()


Example:

task.mark_as_done()  # status= DONE, completed_at = now, updated_at = now


Design Patterns: Separation of concerns, Repository pattern, Enums.

Part 2 — Task Prioritization

Initial Understanding:

TaskPriority Enum defines 4 levels: LOW=1, MEDIUM=2, HIGH=3, URGENT=4.

create_task() converts integer → Enum member.

list_tasks() calls get_tasks_by_priority() to filter tasks by priority.

Example:

TaskPriority(3)  # HIGH


What We Learned:

Priority stored as Enum in Task object allows comparison/filtering.

TaskManager.create_task() ensures consistency.

TaskStorage.get_tasks_by_priority() filters tasks efficiently.

Part 3 — Task Completion Data Flow

Entry Point:

CLI command: status <task_id> done calls TaskManager.update_task_status()

State Changes:

task.mark_as_done() updates: status=DONE, completed_at=now, updated_at=now

Persistence:

TaskStorage.save() writes updated task to tasks.json using TaskEncoder

Enums → stored as strings, datetime → ISO format

Potential Failure Points:

Invalid task ID → no update

Corrupted/missing tasks.json → save/load error

Simultaneous writes → not thread-safe

Part 4 — Reflection & Insights

Architecture Overview:
CLI → TaskManager → TaskStorage → Task (Model) → tasks.json

Feature Highlights:

Task creation, priority filtering, completion

JSON persistence with encoder/decoder

Enums enforce controlled states

Separation of concerns ensures modularity

Challenges & Learning:

DONE status involves timestamps, not just status change

Guided prompts helped map execution flow and storage interactions

Flow Diagram:

              ┌────────────┐
              │    CLI     │  ← User commands (create, status, list)
              └─────┬──────┘
                    │
                    ▼
           ┌─────────────────┐
           │  TaskManager    │  ← Business logic
           │ create_task()   │
           │ update_task_status() │
           │ list_tasks()    │
           └─────┬───────────┘
                 │
                 ▼
           ┌───────────────┐
           │  TaskStorage  │  ← Persistence layer (JSON)
           │ save()        │
           │ get_task()    │
           └─────┬─────────┘
                 │
                 ▼
             tasks.json
        (Tasks persisted with status, priority, timestamps)

Q&A Section (Part 2–4 Questions & Answers)

1. How does the application handle invalid priority values passed to create_task()?
Priority levels range from 1 to 4. If a value outside this range is passed, it may raise an error or default to a specific priority level depending on how create_task() validates input.

2. How is status DONE special and what was the misconception?
DONE triggers mark_as_done(), which updates status, completed_at, and updated_at. Misconception: marking as DONE only changes status, but it also updates timestamps to reflect completion.

3. Are there constraints on priority levels? Can a task have multiple priorities or change priority?
A task has only one priority at a time (Enum). Priority can be changed after creation using update_task_priority().

4. How does priority affect sorting or display in the CLI?
Priority can be used to sort tasks, e.g., URGENT first, then HIGH, MEDIUM, LOW, ensuring critical tasks appear at the top.

5. How are tasks stored in JSON format regarding priority?
Priority is stored as a string (e.g., "HIGH") via encoder. Integer values can also be stored but string representation is preferred for readability.

6. Example JSON Representations:

String Representation:

{
  "title": "Complete project proposal",
  "description": "submit assignment by end of week",
  "priority": "HIGH",
  "status": "TODO"
}


Integer Representation:

{
  "title": "Complete project proposal",
  "description": "submit assignment by end of week",
  "priority": 3,
  "status": "TODO"
}                                                         
