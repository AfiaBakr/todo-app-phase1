# CLI Contracts: Core Todo Operations

**Feature**: Core Todo Operations
**Date**: 2025-12-29
**Status**: Complete

## Overview

This document defines the exact input/output contracts for all CLI commands. These contracts are the source of truth for implementation and testing.

---

## Command Contracts

### 1. `todo add`

**Purpose**: Create a new task

**Signature**:
```
todo add <title> [--description <desc>]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Task title (positional) |
| `--description` | string | No | Task description (default: "") |

**Success Output** (stdout):
```
Task T001 created: "Buy groceries"
```

**Error Outputs** (stderr):
| Condition | Output |
|-----------|--------|
| No title provided | `Error: Task title is required. Usage: todo add <title> [--description <desc>]` |
| Empty title | `Error: Task title cannot be empty` |
| Title > 200 chars | `Error: Title cannot exceed 200 characters` |
| Description > 1000 chars | `Error: Description cannot exceed 1000 characters` |

**Exit Codes**:
- `0` - Success
- `1` - Validation error

---

### 2. `todo list`

**Purpose**: List all tasks

**Signature**:
```
todo list [--filter <pending|completed>] [--verbose]
```

**Options**:
| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--filter` | enum | No | Filter by status: `pending` or `completed` |
| `--verbose` | flag | No | Show detailed output with descriptions |

**Success Output - Empty List** (stdout):
```
No tasks found. Use 'todo add <title>' to create one.
```

**Success Output - Standard** (stdout):
```
Tasks (2 total):
[ ] T001: Buy groceries
[x] T002: Call mom
```

**Success Output - Filtered** (stdout):
```
Tasks (1 pending):
[ ] T001: Buy groceries
```

```
Tasks (1 completed):
[x] T002: Call mom
```

**Success Output - Verbose** (stdout):
```
Tasks (2 total):
[ ] T001: Buy groceries
    Description: Milk, eggs, bread
    Created: 2025-12-29T10:30:00
[x] T002: Call mom
    Description: -
    Created: 2025-12-29T10:35:00
```

**Exit Codes**:
- `0` - Success (always)

---

### 3. `todo view`

**Purpose**: View a single task's details

**Signature**:
```
todo view <task_id>
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | string | Yes | Task ID (e.g., T001) |

**Success Output** (stdout):
```
Task T001
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending
Created: 2025-12-29T10:30:00
```

Or for completed task:
```
Task T001
Title: Buy groceries
Description: Milk, eggs, bread
Status: Complete
Created: 2025-12-29T10:30:00
```

**Error Outputs** (stderr):
| Condition | Output |
|-----------|--------|
| No ID provided | `Error: Task ID required. Usage: todo view <task_id>` |
| Invalid ID format | `Error: Invalid task ID format. Expected format: T###` |
| Task not found | `Error: Task T999 not found` |

**Exit Codes**:
- `0` - Success
- `1` - Error

---

### 4. `todo update`

**Purpose**: Update a task's title and/or description

**Signature**:
```
todo update <task_id> [--title <title>] [--description <desc>]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | string | Yes | Task ID (e.g., T001) |
| `--title` | string | No | New title |
| `--description` | string | No | New description |

**Success Output** (stdout):
```
Task T001 updated: "New title"
```

**Error Outputs** (stderr):
| Condition | Output |
|-----------|--------|
| No ID provided | `Error: Task ID required. Usage: todo update <task_id> [--title <title>] [--description <desc>]` |
| No changes specified | `Error: No changes specified. Use --title or --description` |
| Invalid ID format | `Error: Invalid task ID format. Expected format: T###` |
| Task not found | `Error: Task T999 not found` |
| Empty title | `Error: Task title cannot be empty` |
| Title > 200 chars | `Error: Title cannot exceed 200 characters` |
| Description > 1000 chars | `Error: Description cannot exceed 1000 characters` |

**Exit Codes**:
- `0` - Success
- `1` - Error

---

### 5. `todo delete`

**Purpose**: Delete a task

**Signature**:
```
todo delete <task_id>
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | string | Yes | Task ID (e.g., T001) |

**Success Output** (stdout):
```
Task T001 deleted: "Buy groceries"
```

**Error Outputs** (stderr):
| Condition | Output |
|-----------|--------|
| No ID provided | `Error: Task ID required. Usage: todo delete <task_id>` |
| Invalid ID format | `Error: Invalid task ID format. Expected format: T###` |
| Task not found | `Error: Task T999 not found` |

**Exit Codes**:
- `0` - Success
- `1` - Error

---

### 6. `todo complete`

**Purpose**: Mark a task as complete

**Signature**:
```
todo complete <task_id>
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | string | Yes | Task ID (e.g., T001) |

**Success Output** (stdout):
```
Task T001 marked complete: "Buy groceries"
```

**Already Complete Output** (stdout):
```
Task T001 is already complete
```

**Error Outputs** (stderr):
| Condition | Output |
|-----------|--------|
| No ID provided | `Error: Task ID required. Usage: todo complete <task_id>` |
| Invalid ID format | `Error: Invalid task ID format. Expected format: T###` |
| Task not found | `Error: Task T999 not found` |

**Exit Codes**:
- `0` - Success (including already complete)
- `1` - Error

---

### 7. `todo incomplete`

**Purpose**: Mark a task as incomplete

**Signature**:
```
todo incomplete <task_id>
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `task_id` | string | Yes | Task ID (e.g., T001) |

**Success Output** (stdout):
```
Task T001 marked incomplete: "Buy groceries"
```

**Already Incomplete Output** (stdout):
```
Task T001 is already incomplete
```

**Error Outputs** (stderr):
| Condition | Output |
|-----------|--------|
| No ID provided | `Error: Task ID required. Usage: todo incomplete <task_id>` |
| Invalid ID format | `Error: Invalid task ID format. Expected format: T###` |
| Task not found | `Error: Task T999 not found` |

**Exit Codes**:
- `0` - Success (including already incomplete)
- `1` - Error

---

## Global Options

| Option | Description |
|--------|-------------|
| `--help` | Show help for any command |
| `--version` | Show application version |

**Help Output Example**:
```
$ todo --help
Usage: todo [OPTIONS] COMMAND [ARGS]...

  The Evolution of Todo - CLI Task Manager

Options:
  --version  Show version and exit.
  --help     Show this message and exit.

Commands:
  add         Create a new task
  complete    Mark a task as complete
  delete      Delete a task
  incomplete  Mark a task as incomplete
  list        List all tasks
  update      Update a task
  view        View a task's details
```

**Version Output**:
```
$ todo --version
todo, version 0.1.0
```

---

## Output Format Rules

### Status Indicators

| Status | Indicator |
|--------|-----------|
| Incomplete | `[ ]` |
| Complete | `[x]` |

### Datetime Format

All datetime values displayed in ISO 8601 format without timezone:
```
2025-12-29T10:30:00
```

### Error Format

All errors written to stderr with prefix:
```
Error: <message>
```

### ID Format

IDs always displayed uppercase:
- Input: `t001`, `T001` → Displayed: `T001`
- Validation pattern: `T\d+` (case-insensitive)

---

## Testing Contract Examples

### Add Command Tests

```python
# Test: Successful add
$ todo add "Buy groceries"
> stdout: Task T001 created: "Buy groceries"
> exit: 0

# Test: Add with description
$ todo add "Buy groceries" --description "Milk, eggs"
> stdout: Task T001 created: "Buy groceries"
> exit: 0

# Test: Empty title
$ todo add ""
> stderr: Error: Task title cannot be empty
> exit: 1
```

### List Command Tests

```python
# Test: Empty list
$ todo list
> stdout: No tasks found. Use 'todo add <title>' to create one.
> exit: 0

# Test: With tasks (after adding)
$ todo list
> stdout:
> Tasks (2 total):
> [ ] T001: Buy groceries
> [ ] T002: Call mom
> exit: 0

# Test: Filter pending
$ todo list --filter pending
> stdout:
> Tasks (1 pending):
> [ ] T001: Buy groceries
> exit: 0
```

### Complete/Incomplete Tests

```python
# Test: Mark complete
$ todo complete T001
> stdout: Task T001 marked complete: "Buy groceries"
> exit: 0

# Test: Already complete
$ todo complete T001
> stdout: Task T001 is already complete
> exit: 0

# Test: Mark incomplete
$ todo incomplete T001
> stdout: Task T001 marked incomplete: "Buy groceries"
> exit: 0
```
