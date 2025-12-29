# Feature Specification: Core Todo Operations

**Feature Branch**: `001-core-todo-operations`
**Created**: 2025-12-29
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0

## Overview

This specification defines the core CRUD operations for the Todo application: Add, View, Update, Delete, and Mark Complete/Incomplete. These operations form the foundation upon which advanced features (recurring tasks, reminders, due dates) will be built.

---

## User Scenarios & Testing

### User Story 1 - Add a New Task (Priority: P1)

As a user, I want to add a new task with a title and optional description so that I can track things I need to do.

**Why this priority**: Adding tasks is the fundamental operation—without it, no other feature has meaning. This is the MVP entry point.

**Independent Test**: Can be fully tested by running `todo add "My task"` and verifying the task appears in the list with a unique ID.

**Acceptance Scenarios**:

1. **Given** an empty task list, **When** user runs `todo add "Buy groceries"`, **Then** a new task is created with:
   - Unique ID (auto-generated, format: `T001`, `T002`, etc.)
   - Title: "Buy groceries"
   - Description: empty string
   - Completed: false
   - Created_at: current datetime (ISO 8601 format)
   - Output confirms: `Task T001 created: "Buy groceries"`

2. **Given** an empty task list, **When** user runs `todo add "Buy groceries" --description "Milk, eggs, bread"`, **Then** task is created with:
   - Title: "Buy groceries"
   - Description: "Milk, eggs, bread"
   - Output confirms: `Task T001 created: "Buy groceries"`

3. **Given** a task list with T001, **When** user runs `todo add "Call mom"`, **Then** new task has ID `T002` (sequential, no gaps).

4. **Given** any state, **When** user runs `todo add ""` (empty title), **Then** error displayed: `Error: Task title cannot be empty`

5. **Given** any state, **When** user runs `todo add` (no arguments), **Then** error displayed: `Error: Task title is required. Usage: todo add <title> [--description <desc>]`

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I want to view all my tasks so that I can see what I need to do.

**Why this priority**: Viewing tasks is essential to verify add/update/delete operations work and to see overall progress.

**Independent Test**: Can be tested by adding tasks and running `todo list` to verify all tasks display correctly.

**Acceptance Scenarios**:

1. **Given** an empty task list, **When** user runs `todo list`, **Then** output shows: `No tasks found. Use 'todo add <title>' to create one.`

2. **Given** tasks exist:
   - T001: "Buy groceries" (incomplete)
   - T002: "Call mom" (complete)

   **When** user runs `todo list`, **Then** output shows:
   ```
   Tasks (2 total):
   [ ] T001: Buy groceries
   [x] T002: Call mom
   ```

3. **Given** tasks exist with descriptions, **When** user runs `todo list --verbose`, **Then** output includes descriptions:
   ```
   Tasks (2 total):
   [ ] T001: Buy groceries
       Description: Milk, eggs, bread
       Created: 2025-12-29T10:30:00
   [x] T002: Call mom
       Description: -
       Created: 2025-12-29T10:35:00
   ```

4. **Given** tasks exist, **When** user runs `todo list --filter pending`, **Then** only incomplete tasks shown.

5. **Given** tasks exist, **When** user runs `todo list --filter completed`, **Then** only completed tasks shown.

---

### User Story 3 - View Single Task (Priority: P2)

As a user, I want to view details of a specific task by ID so that I can see all information about it.

**Why this priority**: Important for verifying individual task state, but list view covers basic needs first.

**Independent Test**: Can be tested by adding a task, then running `todo view T001` to see full details.

**Acceptance Scenarios**:

1. **Given** task T001 exists with title "Buy groceries", description "Milk, eggs", created at 2025-12-29T10:30:00, completed=false, **When** user runs `todo view T001`, **Then** output shows:
   ```
   Task T001
   Title: Buy groceries
   Description: Milk, eggs
   Status: Pending
   Created: 2025-12-29T10:30:00
   ```

2. **Given** no task with ID T999 exists, **When** user runs `todo view T999`, **Then** error: `Error: Task T999 not found`

3. **Given** any state, **When** user runs `todo view` (no ID), **Then** error: `Error: Task ID required. Usage: todo view <task_id>`

---

### User Story 4 - Update a Task (Priority: P2)

As a user, I want to update a task's title or description so that I can correct or refine my tasks.

**Why this priority**: Allows fixing mistakes; less critical than add/view but important for usability.

**Independent Test**: Can be tested by adding a task, updating it, then viewing to confirm changes.

**Acceptance Scenarios**:

1. **Given** task T001 exists with title "Buy groceries", **When** user runs `todo update T001 --title "Buy organic groceries"`, **Then**:
   - Task title updated to "Buy organic groceries"
   - Output: `Task T001 updated: "Buy organic groceries"`

2. **Given** task T001 exists with empty description, **When** user runs `todo update T001 --description "From farmers market"`, **Then**:
   - Description updated to "From farmers market"
   - Output: `Task T001 updated: "Buy groceries"`

3. **Given** task T001 exists, **When** user runs `todo update T001 --title "New title" --description "New desc"`, **Then** both fields updated.

4. **Given** no task T999 exists, **When** user runs `todo update T999 --title "Test"`, **Then** error: `Error: Task T999 not found`

5. **Given** task T001 exists, **When** user runs `todo update T001` (no changes specified), **Then** error: `Error: No changes specified. Use --title or --description`

6. **Given** task T001 exists, **When** user runs `todo update T001 --title ""` (empty title), **Then** error: `Error: Task title cannot be empty`

---

### User Story 5 - Delete a Task (Priority: P2)

As a user, I want to delete a task so that I can remove tasks I no longer need.

**Why this priority**: Essential for task management but less frequent than add/view operations.

**Independent Test**: Can be tested by adding a task, deleting it, then listing to confirm removal.

**Acceptance Scenarios**:

1. **Given** task T001 exists with title "Buy groceries", **When** user runs `todo delete T001`, **Then**:
   - Task is removed from storage
   - Output: `Task T001 deleted: "Buy groceries"`

2. **Given** no task T999 exists, **When** user runs `todo delete T999`, **Then** error: `Error: Task T999 not found`

3. **Given** any state, **When** user runs `todo delete` (no ID), **Then** error: `Error: Task ID required. Usage: todo delete <task_id>`

4. **Given** tasks T001, T002, T003 exist, **When** user deletes T002, **Then** T001 and T003 remain; IDs are NOT renumbered.

---

### User Story 6 - Mark Task Complete (Priority: P1)

As a user, I want to mark a task as complete so that I can track my progress.

**Why this priority**: Core to the todo concept—tracking completion is why todo apps exist.

**Independent Test**: Can be tested by adding a task, marking complete, then listing to see [x] status.

**Acceptance Scenarios**:

1. **Given** task T001 exists with completed=false, **When** user runs `todo complete T001`, **Then**:
   - Task completed set to true
   - Output: `Task T001 marked complete: "Buy groceries"`

2. **Given** task T001 exists with completed=true, **When** user runs `todo complete T001`, **Then**:
   - Task remains completed=true (idempotent)
   - Output: `Task T001 is already complete`

3. **Given** no task T999 exists, **When** user runs `todo complete T999`, **Then** error: `Error: Task T999 not found`

---

### User Story 7 - Mark Task Incomplete (Priority: P2)

As a user, I want to mark a completed task as incomplete so that I can reopen tasks if needed.

**Why this priority**: Less common operation but necessary for correcting mistakes.

**Independent Test**: Can be tested by completing a task, then marking incomplete, then listing.

**Acceptance Scenarios**:

1. **Given** task T001 exists with completed=true, **When** user runs `todo incomplete T001`, **Then**:
   - Task completed set to false
   - Output: `Task T001 marked incomplete: "Buy groceries"`

2. **Given** task T001 exists with completed=false, **When** user runs `todo incomplete T001`, **Then**:
   - Task remains completed=false (idempotent)
   - Output: `Task T001 is already incomplete`

3. **Given** no task T999 exists, **When** user runs `todo incomplete T999`, **Then** error: `Error: Task T999 not found`

---

### Edge Cases

**ID Handling**:
- Task IDs are case-insensitive: `t001`, `T001`, `t001` all refer to the same task
- Invalid ID format (e.g., `todo view abc`) returns: `Error: Invalid task ID format. Expected format: T###`

**Title/Description Limits**:
- Title max length: 200 characters. If exceeded: `Error: Title cannot exceed 200 characters`
- Description max length: 1000 characters. If exceeded: `Error: Description cannot exceed 1000 characters`

**Whitespace Handling**:
- Leading/trailing whitespace in titles is trimmed
- Title of only whitespace treated as empty: `Error: Task title cannot be empty`

**Concurrent State**:
- In-memory storage is single-threaded; no concurrency concerns in this phase

**Persistence**:
- Data is NOT persisted between sessions (in-memory only)
- On startup, task list is empty
- If persistence is needed later, it will be a separate spec

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST store tasks in memory with unique, sequential IDs (format: T###)
- **FR-002**: System MUST support adding tasks with title (required) and description (optional)
- **FR-003**: System MUST support listing all tasks with completion status indicators
- **FR-004**: System MUST support viewing a single task's full details by ID
- **FR-005**: System MUST support updating task title and/or description
- **FR-006**: System MUST support deleting tasks by ID
- **FR-007**: System MUST support marking tasks complete/incomplete
- **FR-008**: System MUST validate all inputs and return clear error messages
- **FR-009**: System MUST preserve task IDs (no renumbering after deletion)
- **FR-010**: System MUST record created_at timestamp in ISO 8601 format

### Non-Functional Requirements

- **NFR-001**: CLI response time MUST be < 100ms for all operations
- **NFR-002**: Error messages MUST be human-readable and actionable
- **NFR-003**: Output MUST be consistent and parseable (future JSON support)

### Key Entities

**Task**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes (auto) | Unique identifier, format T### (e.g., T001) |
| title | string | Yes | Task title, 1-200 characters |
| description | string | No | Task description, 0-1000 characters |
| completed | boolean | Yes (default: false) | Completion status |
| created_at | datetime | Yes (auto) | ISO 8601 timestamp when created |

**Future Fields** (not implemented in this spec, reserved for advanced features):
- due_date: datetime (optional)
- recurrence: string (optional) - e.g., "daily", "weekly"
- priority: enum (optional) - low, medium, high
- tags: list[string] (optional)
- reminder_at: datetime (optional)

---

## CLI Command Reference

### Command Summary

| Command | Description | Arguments |
|---------|-------------|-----------|
| `todo add <title>` | Create new task | `--description <desc>` |
| `todo list` | List all tasks | `--filter <pending\|completed>`, `--verbose` |
| `todo view <id>` | View task details | - |
| `todo update <id>` | Update task | `--title <title>`, `--description <desc>` |
| `todo delete <id>` | Delete task | - |
| `todo complete <id>` | Mark complete | - |
| `todo incomplete <id>` | Mark incomplete | - |

### Global Options

| Option | Description |
|--------|-------------|
| `--help` | Show help for command |
| `--version` | Show app version |

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 7 user stories pass their acceptance scenarios
- **SC-002**: All edge cases are handled with appropriate error messages
- **SC-003**: CLI responds to all commands in < 100ms
- **SC-004**: Code coverage of business logic is > 90%
- **SC-005**: Zero manual code edits required—all code generated from this spec

### Definition of Done

- [ ] All acceptance scenarios pass as automated tests
- [ ] All error messages match specification exactly
- [ ] CLI help text accurately describes all commands
- [ ] Code follows Python 3.13+ best practices
- [ ] Code is generated from spec (no manual implementation)

---

## Technical Notes

### ID Generation Strategy

- IDs are sequential integers with T prefix: T001, T002, T003...
- Counter persists in memory; starts at 1 on application start
- Deleted IDs are NOT reused within a session
- IDs are displayed with zero-padding to 3 digits (T001-T999)
- If > 999 tasks, expand format: T1000, T1001, etc.

### Output Format

Standard output format for task listing:
```
[status] ID: Title
```

Where status is:
- `[ ]` for incomplete
- `[x]` for complete

### Error Output

All errors go to stderr with format:
```
Error: <message>
```

Success messages go to stdout.

---

## Appendix: Sample Session

```bash
$ todo list
No tasks found. Use 'todo add <title>' to create one.

$ todo add "Buy groceries" --description "Milk, eggs, bread"
Task T001 created: "Buy groceries"

$ todo add "Call mom"
Task T002 created: "Call mom"

$ todo list
Tasks (2 total):
[ ] T001: Buy groceries
[ ] T002: Call mom

$ todo complete T001
Task T001 marked complete: "Buy groceries"

$ todo list
Tasks (2 total):
[x] T001: Buy groceries
[ ] T002: Call mom

$ todo list --filter pending
Tasks (1 pending):
[ ] T002: Call mom

$ todo view T001
Task T001
Title: Buy groceries
Description: Milk, eggs, bread
Status: Complete
Created: 2025-12-29T10:30:00

$ todo update T002 --title "Call mom and dad"
Task T002 updated: "Call mom and dad"

$ todo delete T001
Task T001 deleted: "Buy groceries"

$ todo list
Tasks (1 total):
[ ] T002: Call mom and dad

$ todo view T001
Error: Task T001 not found
```
