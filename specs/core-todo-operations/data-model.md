# Data Model: Core Todo Operations

**Feature**: Core Todo Operations
**Date**: 2025-12-29
**Status**: Complete

## Overview

This document defines the data model for the Core Todo Operations feature. All entities, validation rules, and state transitions are derived from the feature specification.

---

## Entities

### Task

The primary entity representing a todo item.

#### Fields

| Field | Type | Required | Default | Mutable | Description |
|-------|------|----------|---------|---------|-------------|
| `id` | `str` | Yes (auto) | Generated | No | Unique identifier, format T### (e.g., T001, T002) |
| `title` | `str` | Yes | - | Yes | Task title, 1-200 characters |
| `description` | `str` | No | `""` | Yes | Task description, 0-1000 characters |
| `completed` | `bool` | Yes | `False` | Yes | Completion status |
| `created_at` | `datetime` | Yes (auto) | Current time | No | ISO 8601 timestamp when task was created |

#### Reserved Fields (Future)

These fields are reserved for advanced features and should NOT be implemented in this phase:

| Field | Type | Purpose |
|-------|------|---------|
| `due_date` | `datetime \| None` | Task deadline |
| `recurrence` | `str \| None` | Recurrence pattern (daily, weekly, etc.) |
| `priority` | `Literal["low", "medium", "high"] \| None` | Task priority |
| `tags` | `list[str]` | Task categorization |
| `reminder_at` | `datetime \| None` | When to remind user |

---

## Validation Rules

### Title Validation

| Rule | Constraint | Error Message |
|------|------------|---------------|
| Required | Cannot be empty or whitespace-only | `Task title cannot be empty` |
| Max length | ≤ 200 characters | `Title cannot exceed 200 characters` |
| Trimming | Leading/trailing whitespace removed | (silent) |

### Description Validation

| Rule | Constraint | Error Message |
|------|------------|---------------|
| Optional | Can be empty string | - |
| Max length | ≤ 1000 characters | `Description cannot exceed 1000 characters` |

### ID Validation

| Rule | Constraint | Error Message |
|------|------------|---------------|
| Format | Must match pattern `T\d+` (case-insensitive) | `Invalid task ID format. Expected format: T###` |
| Existence | Must exist in storage for view/update/delete | `Task {id} not found` |

---

## State Transitions

### Task Lifecycle

```
┌─────────────────────────────────────────┐
│                 Created                  │
│            (completed=False)             │
└─────────────┬───────────────────────────┘
              │
              │ todo complete T###
              ▼
┌─────────────────────────────────────────┐
│                Completed                 │
│            (completed=True)              │
└─────────────┬───────────────────────────┘
              │
              │ todo incomplete T###
              ▼
┌─────────────────────────────────────────┐
│                 Pending                  │
│            (completed=False)             │
└─────────────────────────────────────────┘
```

### Completion State Machine

| Current State | Action | New State | Output |
|--------------|--------|-----------|--------|
| completed=False | `complete` | completed=True | `Task {id} marked complete: "{title}"` |
| completed=True | `complete` | completed=True | `Task {id} is already complete` |
| completed=True | `incomplete` | completed=False | `Task {id} marked incomplete: "{title}"` |
| completed=False | `incomplete` | completed=False | `Task {id} is already incomplete` |

---

## ID Generation

### Format

- Pattern: `T` followed by digits
- Standard display: `T001`, `T002`, ..., `T999`
- Extended display: `T1000`, `T1001`, ... (when exceeding 999)

### Rules

1. IDs are assigned sequentially starting from 1
2. Counter is maintained per application session
3. Counter resets to 0 on application restart (in-memory)
4. Deleted IDs are NOT reused within a session
5. ID comparison is case-insensitive (`T001` == `t001`)

### Implementation

```python
class IDGenerator:
    def __init__(self):
        self._counter: int = 0

    def next(self) -> str:
        self._counter += 1
        if self._counter <= 999:
            return f"T{self._counter:03d}"
        return f"T{self._counter}"

    def reset(self) -> None:
        self._counter = 0
```

---

## Python Implementation

### Task Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    """
    Represents a todo task.

    Immutable fields: id, created_at
    Mutable fields: title, description, completed
    """
    id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Normalize ID to uppercase."""
        object.__setattr__(self, 'id', self.id.upper())
```

### Exception Classes

```python
class TodoError(Exception):
    """Base exception for todo application."""
    pass

class TaskNotFoundError(TodoError):
    """Raised when a task with given ID does not exist."""
    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")

class ValidationError(TodoError):
    """Raised when input validation fails."""
    pass

class EmptyTitleError(ValidationError):
    """Raised when task title is empty."""
    def __init__(self):
        super().__init__("Task title cannot be empty")

class TitleTooLongError(ValidationError):
    """Raised when task title exceeds 200 characters."""
    def __init__(self):
        super().__init__("Title cannot exceed 200 characters")

class DescriptionTooLongError(ValidationError):
    """Raised when description exceeds 1000 characters."""
    def __init__(self):
        super().__init__("Description cannot exceed 1000 characters")

class InvalidIDFormatError(ValidationError):
    """Raised when task ID format is invalid."""
    def __init__(self):
        super().__init__("Invalid task ID format. Expected format: T###")
```

---

## Storage Model

### TaskService

```python
from typing import Iterator

class TaskService:
    """
    In-memory storage and operations for tasks.

    Storage: dict[str, Task] with uppercase ID as key
    ID Generator: Sequential counter
    """

    def __init__(self):
        self._tasks: dict[str, Task] = {}
        self._id_generator = IDGenerator()

    # CRUD Operations
    def add(self, title: str, description: str = "") -> Task: ...
    def get(self, task_id: str) -> Task: ...
    def list_all(self) -> list[Task]: ...
    def update(self, task_id: str, title: str | None = None,
               description: str | None = None) -> Task: ...
    def delete(self, task_id: str) -> Task: ...

    # State Operations
    def mark_complete(self, task_id: str) -> tuple[Task, bool]: ...
    def mark_incomplete(self, task_id: str) -> tuple[Task, bool]: ...

    # Query Operations
    def list_pending(self) -> list[Task]: ...
    def list_completed(self) -> list[Task]: ...
    def count(self) -> int: ...
```

---

## Relationships

This phase has a single entity (Task) with no relationships.

Future phases may introduce:
- Task → Tags (many-to-many)
- Task → Project (many-to-one)
- Task → Subtasks (one-to-many)

---

## Serialization (Future)

When persistence is added, Task will serialize to:

```json
{
  "id": "T001",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-29T10:30:00"
}
```

ISO 8601 format for datetime fields.
