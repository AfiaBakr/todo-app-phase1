# Research: Core Todo Operations

**Feature**: Core Todo Operations
**Date**: 2025-12-29
**Status**: Complete

## Overview

This document captures research findings for implementing the Core Todo Operations CLI application in Python.

---

## Technology Decisions

### 1. CLI Framework

**Decision**: Typer

**Rationale**:
- Modern CLI framework built on Click
- Automatic argument/option parsing from type hints
- Built-in help generation from docstrings
- Native support for Python 3.13+ type system
- Rich integration for enhanced terminal output (optional)

**Alternatives Considered**:

| Framework | Pros | Cons | Why Rejected |
|-----------|------|------|--------------|
| argparse | Stdlib, no dependencies | Verbose, manual help text | More boilerplate |
| Click | Mature, well-documented | Less ergonomic than Typer | Typer is built on Click with improvements |
| Fire | Auto-generates CLI | Less control over help/output | Doesn't match our exact output requirements |

**Implementation Notes**:
```python
import typer
app = typer.Typer()

@app.command()
def add(title: str, description: str = ""):
    """Create a new task."""
    ...
```

---

### 2. Data Model

**Decision**: Python dataclasses

**Rationale**:
- Native to Python 3.13+
- Automatic `__init__`, `__repr__`, `__eq__`
- Type hints enforced at definition
- Field defaults supported
- Compatible with future JSON serialization

**Alternatives Considered**:

| Approach | Pros | Cons | Why Rejected |
|----------|------|------|--------------|
| Pydantic | Validation, JSON support | External dep, overkill for in-memory | Unnecessary complexity |
| NamedTuple | Immutable, lightweight | Cannot update fields | Need mutable title/description |
| Plain class | Full control | More boilerplate | Dataclass provides same with less code |
| TypedDict | JSON-like | No methods, no validation | Need encapsulated behavior |

**Implementation Notes**:
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

---

### 3. Storage Strategy

**Decision**: In-memory dictionary with TaskService class

**Rationale**:
- `dict[str, Task]` provides O(1) lookup by ID
- Simple iteration for list operations
- No external dependencies
- Single source of truth for task state
- Easy to swap for persistent storage later

**Alternatives Considered**:

| Approach | Pros | Cons | Why Rejected |
|----------|------|------|--------------|
| List | Simple | O(n) lookup by ID | Performance for view/update/delete |
| SQLite in-memory | SQL queries | External complexity | Overkill for MVP |
| shelve | Persistent dict | File I/O complexity | Out of scope for this phase |

**Implementation Notes**:
```python
class TaskService:
    def __init__(self):
        self._tasks: dict[str, Task] = {}
        self._counter: int = 0

    def add(self, title: str, description: str = "") -> Task:
        self._counter += 1
        task_id = f"T{self._counter:03d}"
        task = Task(id=task_id, title=title, description=description)
        self._tasks[task_id] = task
        return task
```

---

### 4. ID Generation

**Decision**: Sequential counter with T### format

**Rationale**:
- Predictable, human-readable IDs
- Zero-padded for consistent width (T001-T999)
- Expands naturally beyond 999 (T1000)
- Counter lives in TaskService instance
- Deleted IDs are NOT reused (per spec)

**Implementation Notes**:
```python
def _generate_id(self) -> str:
    self._counter += 1
    if self._counter <= 999:
        return f"T{self._counter:03d}"
    return f"T{self._counter}"
```

---

### 5. Error Handling

**Decision**: Custom exception classes + CLI error formatting

**Rationale**:
- Domain-specific exceptions for clear error types
- CLI layer catches and formats to stderr
- Consistent "Error: <message>" format per spec

**Exception Hierarchy**:
```python
class TodoError(Exception):
    """Base exception for todo app."""
    pass

class TaskNotFoundError(TodoError):
    """Raised when task ID doesn't exist."""
    pass

class ValidationError(TodoError):
    """Raised when input validation fails."""
    pass
```

---

### 6. Testing Strategy

**Decision**: pytest with fixtures and separate test directories

**Rationale**:
- pytest is the de facto Python testing framework
- Fixtures enable clean test setup
- Separate directories for unit/integration/contract tests
- pytest-cov for coverage measurement

**Test Structure**:
```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_task_model.py   # Task dataclass tests
│   ├── test_task_service.py # Service logic tests
│   └── test_validators.py   # Validation tests
├── integration/
│   └── test_cli_commands.py # End-to-end CLI tests
└── contract/
    └── test_cli_contracts.py # Output format tests
```

---

## Dependencies

### Production Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| typer | >=0.9.0 | CLI framework |
| rich | >=13.0.0 | Terminal formatting (optional) |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=8.0.0 | Testing framework |
| pytest-cov | >=4.0.0 | Coverage measurement |

### pyproject.toml Template

```toml
[project]
name = "todo-app"
version = "0.1.0"
description = "Advanced-level CLI Todo application"
requires-python = ">=3.13"
dependencies = [
    "typer>=0.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
]

[project.scripts]
todo = "src.cli.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Best Practices Applied

### 1. Separation of Concerns

```
CLI Layer (cli/main.py)
    ↓ calls
Service Layer (services/task_service.py)
    ↓ uses
Model Layer (models/task.py)
```

- CLI handles input parsing and output formatting
- Service handles business logic and storage
- Model defines data structure only

### 2. Single Responsibility

Each module has one job:
- `task.py` - Define Task structure
- `task_service.py` - CRUD operations on tasks
- `main.py` - CLI command definitions
- `validators.py` - Input validation rules
- `id_generator.py` - ID generation logic

### 3. Dependency Injection Ready

TaskService can be injected into CLI for testing:
```python
# Production
app = create_app(TaskService())

# Testing
app = create_app(MockTaskService())
```

---

## Open Questions (Resolved)

| Question | Resolution |
|----------|------------|
| Which CLI framework? | Typer - best ergonomics for type hints |
| Dataclass vs Pydantic? | Dataclass - simpler, no external validation needed |
| How to handle errors? | Custom exceptions + CLI formatting |
| Test isolation? | Fresh TaskService instance per test |

---

## References

- [Typer Documentation](https://typer.tiangolo.com/)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [pytest Documentation](https://docs.pytest.org/)
