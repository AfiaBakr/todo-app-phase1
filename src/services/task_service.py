"""Task service for managing todo tasks.

TaskService provides all CRUD operations for tasks and maintains
persistent storage via JSON file. It is the single source of truth for task state.
"""

import json
from datetime import datetime
from pathlib import Path

from src.models.task import Task
from src.lib.id_generator import IDGenerator
from src.lib.validators import validate_title, validate_description, validate_task_id
from src.lib.exceptions import TaskNotFoundError, NoChangesSpecifiedError

# Default storage file location
DEFAULT_STORAGE_FILE = Path.home() / ".todo_tasks.json"


class TaskService:
    """Persistent storage and operations for tasks.

    The service maintains a dictionary of tasks keyed by uppercase task ID.
    Tasks are automatically saved to a JSON file after each modification.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects.
        _id_generator: Sequential ID generator for new tasks.
        _storage_file: Path to the JSON file for persistence.

    Example:
        >>> service = TaskService()
        >>> task = service.add("Buy groceries", "Milk, eggs")
        >>> task.id
        'T001'
        >>> service.get("T001").title
        'Buy groceries'
    """

    def __init__(self, storage_file: Path | None = None) -> None:
        """Initialize the service and load existing tasks from file."""
        self._storage_file = storage_file or DEFAULT_STORAGE_FILE
        self._tasks: dict[str, Task] = {}
        self._id_generator = IDGenerator()
        self._load()

    # ============================================================
    # Persistence Operations
    # ============================================================

    def _load(self) -> None:
        """Load tasks from the JSON storage file."""
        if not self._storage_file.exists():
            return

        try:
            with open(self._storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Restore tasks
            for task_data in data.get("tasks", []):
                task = Task(
                    id=task_data["id"],
                    title=task_data["title"],
                    description=task_data.get("description", ""),
                    completed=task_data.get("completed", False),
                    created_at=datetime.fromisoformat(task_data["created_at"]),
                )
                self._tasks[task.id] = task

            # Restore ID counter
            counter = data.get("next_id_counter", 0)
            self._id_generator.set_counter(counter)

        except (json.JSONDecodeError, KeyError):
            # If file is corrupted, start fresh
            pass

    def _save(self) -> None:
        """Save tasks to the JSON storage file."""
        data = {
            "next_id_counter": self._id_generator.current(),
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.format_created_at(),
                }
                for task in self._tasks.values()
            ],
        }

        with open(self._storage_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ============================================================
    # CRUD Operations
    # ============================================================

    def add(self, title: str, description: str = "") -> Task:
        """Create a new task with the given title and description.

        Args:
            title: The task title (required, 1-200 chars).
            description: The task description (optional, 0-1000 chars).

        Returns:
            The newly created Task object.

        Raises:
            EmptyTitleError: If title is empty or whitespace-only.
            TitleTooLongError: If title exceeds 200 characters.
            DescriptionTooLongError: If description exceeds 1000 characters.
        """
        # Validate inputs
        title = validate_title(title)
        description = validate_description(description)

        # Generate ID and create task
        task_id = self._id_generator.next()
        task = Task(id=task_id, title=title, description=description)

        # Store task and save
        self._tasks[task_id] = task
        self._save()
        return task

    def get(self, task_id: str) -> Task:
        """Get a task by its ID.

        Args:
            task_id: The task ID to look up (case-insensitive).

        Returns:
            The Task object with the given ID.

        Raises:
            InvalidIDFormatError: If task_id format is invalid.
            TaskNotFoundError: If no task exists with the given ID.
        """
        task_id = validate_task_id(task_id)
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]

    def list_all(self) -> list[Task]:
        """Get all tasks ordered by ID.

        Returns:
            List of all tasks, sorted by task ID.
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The task ID to update.
            title: New title (optional, None means no change).
            description: New description (optional, None means no change).

        Returns:
            The updated Task object.

        Raises:
            InvalidIDFormatError: If task_id format is invalid.
            TaskNotFoundError: If no task exists with the given ID.
            NoChangesSpecifiedError: If neither title nor description is provided.
            EmptyTitleError: If title is empty or whitespace-only.
            TitleTooLongError: If title exceeds 200 characters.
            DescriptionTooLongError: If description exceeds 1000 characters.
        """
        # Check that at least one change is specified
        if title is None and description is None:
            raise NoChangesSpecifiedError()

        # Get the task (validates ID and existence)
        task = self.get(task_id)

        # Update fields if provided
        if title is not None:
            task.title = validate_title(title)
        if description is not None:
            task.description = validate_description(description)

        self._save()
        return task

    def delete(self, task_id: str) -> Task:
        """Delete a task by its ID.

        Args:
            task_id: The task ID to delete.

        Returns:
            The deleted Task object (for confirmation message).

        Raises:
            InvalidIDFormatError: If task_id format is invalid.
            TaskNotFoundError: If no task exists with the given ID.
        """
        task_id = validate_task_id(task_id)
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        task = self._tasks.pop(task_id)
        self._save()
        return task

    # ============================================================
    # State Operations
    # ============================================================

    def mark_complete(self, task_id: str) -> tuple[Task, bool]:
        """Mark a task as complete.

        Args:
            task_id: The task ID to mark complete.

        Returns:
            Tuple of (Task, changed) where changed is True if the
            state actually changed, False if already complete.

        Raises:
            InvalidIDFormatError: If task_id format is invalid.
            TaskNotFoundError: If no task exists with the given ID.
        """
        task = self.get(task_id)
        if task.completed:
            return task, False
        task.completed = True
        self._save()
        return task, True

    def mark_incomplete(self, task_id: str) -> tuple[Task, bool]:
        """Mark a task as incomplete.

        Args:
            task_id: The task ID to mark incomplete.

        Returns:
            Tuple of (Task, changed) where changed is True if the
            state actually changed, False if already incomplete.

        Raises:
            InvalidIDFormatError: If task_id format is invalid.
            TaskNotFoundError: If no task exists with the given ID.
        """
        task = self.get(task_id)
        if not task.completed:
            return task, False
        task.completed = False
        self._save()
        return task, True

    # ============================================================
    # Query Operations
    # ============================================================

    def list_pending(self) -> list[Task]:
        """Get all incomplete tasks ordered by ID.

        Returns:
            List of tasks where completed=False, sorted by ID.
        """
        return [t for t in self.list_all() if not t.completed]

    def list_completed(self) -> list[Task]:
        """Get all completed tasks ordered by ID.

        Returns:
            List of tasks where completed=True, sorted by ID.
        """
        return [t for t in self.list_all() if t.completed]

    def count(self) -> int:
        """Get the total number of tasks.

        Returns:
            The number of tasks in storage.
        """
        return len(self._tasks)
