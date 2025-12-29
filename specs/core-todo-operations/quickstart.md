# Quickstart: Core Todo Operations

**Feature**: Core Todo Operations
**Date**: 2025-12-29

## Prerequisites

- Python 3.13+
- UV package manager

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd todo_phase1
```

### 2. Install dependencies with UV

```bash
# Install UV if not already installed
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"
```

### 3. Activate the virtual environment

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

---

## Usage

### Add a Task

```bash
# Simple task
todo add "Buy groceries"
# Output: Task T001 created: "Buy groceries"

# Task with description
todo add "Buy groceries" --description "Milk, eggs, bread"
# Output: Task T001 created: "Buy groceries"
```

### List Tasks

```bash
# List all tasks
todo list
# Output:
# Tasks (2 total):
# [ ] T001: Buy groceries
# [ ] T002: Call mom

# List with details
todo list --verbose
# Output:
# Tasks (2 total):
# [ ] T001: Buy groceries
#     Description: Milk, eggs, bread
#     Created: 2025-12-29T10:30:00
# [ ] T002: Call mom
#     Description: -
#     Created: 2025-12-29T10:35:00

# Filter by status
todo list --filter pending
todo list --filter completed
```

### View a Task

```bash
todo view T001
# Output:
# Task T001
# Title: Buy groceries
# Description: Milk, eggs, bread
# Status: Pending
# Created: 2025-12-29T10:30:00
```

### Update a Task

```bash
# Update title
todo update T001 --title "Buy organic groceries"
# Output: Task T001 updated: "Buy organic groceries"

# Update description
todo update T001 --description "From farmers market"
# Output: Task T001 updated: "Buy organic groceries"

# Update both
todo update T001 --title "New title" --description "New description"
```

### Complete a Task

```bash
todo complete T001
# Output: Task T001 marked complete: "Buy groceries"

# Already complete (idempotent)
todo complete T001
# Output: Task T001 is already complete
```

### Reopen a Task

```bash
todo incomplete T001
# Output: Task T001 marked incomplete: "Buy groceries"
```

### Delete a Task

```bash
todo delete T001
# Output: Task T001 deleted: "Buy groceries"
```

### Help

```bash
# General help
todo --help

# Command-specific help
todo add --help
todo list --help
```

---

## Sample Session

Here's a complete session demonstrating all features:

```bash
$ todo list
No tasks found. Use 'todo add <title>' to create one.

$ todo add "Buy groceries" --description "Milk, eggs, bread"
Task T001 created: "Buy groceries"

$ todo add "Call mom"
Task T002 created: "Call mom"

$ todo add "Pay bills"
Task T003 created: "Pay bills"

$ todo list
Tasks (3 total):
[ ] T001: Buy groceries
[ ] T002: Call mom
[ ] T003: Pay bills

$ todo complete T001
Task T001 marked complete: "Buy groceries"

$ todo list
Tasks (3 total):
[x] T001: Buy groceries
[ ] T002: Call mom
[ ] T003: Pay bills

$ todo list --filter pending
Tasks (2 pending):
[ ] T002: Call mom
[ ] T003: Pay bills

$ todo view T001
Task T001
Title: Buy groceries
Description: Milk, eggs, bread
Status: Complete
Created: 2025-12-29T10:30:00

$ todo update T002 --title "Call mom and dad"
Task T002 updated: "Call mom and dad"

$ todo delete T003
Task T003 deleted: "Pay bills"

$ todo list
Tasks (2 total):
[x] T001: Buy groceries
[ ] T002: Call mom and dad
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_task_service.py

# Run with verbose output
pytest -v
```

---

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Task title cannot be empty` | Empty or whitespace-only title | Provide a valid title |
| `Task T999 not found` | ID doesn't exist | Check ID with `todo list` |
| `Invalid task ID format` | Wrong ID format (e.g., "abc") | Use format T### (e.g., T001) |
| `No changes specified` | Update without --title or --description | Specify what to update |

---

## Development

### Project Structure

```
todo_phase1/
├── src/
│   ├── models/task.py           # Task dataclass
│   ├── services/task_service.py # Business logic
│   ├── cli/main.py              # CLI commands
│   └── lib/                     # Utilities
├── tests/
│   ├── unit/                    # Unit tests
│   ├── integration/             # CLI tests
│   └── contract/                # Output format tests
├── specs/
│   └── core-todo-operations/    # This feature
├── pyproject.toml               # Project config
└── README.md                    # Project docs
```

### Adding a Feature

1. Create spec in `specs/<feature-name>/spec.md`
2. Run `/sp.plan` to create implementation plan
3. Run `/sp.tasks` to generate task list
4. Generate code from spec (no manual coding)
5. Validate against acceptance criteria
