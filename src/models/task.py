"""Task model for the Todo application.

The Task dataclass represents a single todo item with all its attributes.
Immutable fields: id, created_at
Mutable fields: title, description, completed
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique identifier in format T### (e.g., T001). Immutable.
        title: Task title, 1-200 characters. Mutable.
        description: Task description, 0-1000 characters. Mutable.
        completed: Whether the task is complete. Mutable.
        created_at: ISO 8601 timestamp when task was created. Immutable.

    Example:
        >>> task = Task(id="T001", title="Buy groceries")
        >>> task.completed
        False
        >>> task.completed = True
        >>> task.completed
        True
    """

    id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Normalize the task ID to uppercase after initialization."""
        # Use object.__setattr__ to work even if frozen=True in future
        object.__setattr__(self, 'id', self.id.upper())

    def format_created_at(self) -> str:
        """Format the created_at timestamp as ISO 8601 string without timezone.

        Returns:
            String in format YYYY-MM-DDTHH:MM:SS (e.g., 2025-12-29T10:30:00)
        """
        return self.created_at.strftime("%Y-%m-%dT%H:%M:%S")

    def status_display(self) -> str:
        """Return the display status for the task.

        Returns:
            "Complete" if completed, "Pending" otherwise.
        """
        return "Complete" if self.completed else "Pending"

    def checkbox_display(self) -> str:
        """Return the checkbox indicator for list display.

        Returns:
            "[x]" if completed, "[ ]" otherwise.
        """
        return "[x]" if self.completed else "[ ]"
