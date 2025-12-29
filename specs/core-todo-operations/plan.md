# Implementation Plan: Core Todo Operations

**Branch**: `001-core-todo-operations` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/core-todo-operations/spec.md`
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0

## Summary

Implement a command-line Todo application with core CRUD operations (Add, View, Update, Delete, Mark Complete/Incomplete). The application uses in-memory storage, sequential task IDs (T###), and follows spec-driven development principles where all code is generated from approved specifications.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**:
- `typer` - Modern CLI framework with automatic help generation
- `rich` - Terminal formatting for clean output (optional, can use plain text)
- Standard library: `datetime`, `dataclasses`, `typing`

**Package Manager**: UV (fast Python package installer)
**Storage**: In-memory (Python dict/list, no external database)
**Testing**: pytest with pytest-cov for coverage
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: < 100ms response time for all operations
**Constraints**: No persistence between sessions, single-threaded
**Scale/Scope**: Personal todo management, < 1000 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-First Development | PASS | Spec complete with data models, commands, edge cases, acceptance criteria |
| II. Pure Code Generation | PASS | All code will be generated from this spec |
| III. Incremental Architecture | PASS | Core CRUD first, advanced features in future specs |
| IV. Test-Driven Quality | PASS | Given/When/Then acceptance scenarios defined |
| V. Explicit State Management | PASS | In-memory storage with unique immutable IDs |
| VI. AI-Native Extensibility | PASS | Task model reserves future fields; CLI-first design |

**Gate Status**: ALL GATES PASS - Proceed with Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/core-todo-operations/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI contracts)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── models/
│   ├── __init__.py
│   └── task.py          # Task dataclass
├── services/
│   ├── __init__.py
│   └── task_service.py  # Business logic (CRUD operations)
├── cli/
│   ├── __init__.py
│   └── main.py          # Typer CLI commands
└── lib/
    ├── __init__.py
    ├── id_generator.py  # Sequential ID generator
    └── validators.py    # Input validation

tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py
│   ├── test_task_service.py
│   └── test_validators.py
├── integration/
│   ├── __init__.py
│   └── test_cli_commands.py
└── contract/
    ├── __init__.py
    └── test_cli_contracts.py
```

**Structure Decision**: Single project layout selected. CLI application with clear separation:
- `models/` - Data structures (Task dataclass)
- `services/` - Business logic (TaskService with in-memory storage)
- `cli/` - Command-line interface (Typer commands)
- `lib/` - Shared utilities (ID generation, validation)

## Complexity Tracking

No constitution violations. Simplest viable architecture selected.

---

## Phase 0: Research Summary

### Technology Decisions

#### CLI Framework: Typer

**Decision**: Use Typer for CLI implementation
**Rationale**:
- Type hints become CLI arguments automatically
- Built-in help generation from docstrings
- Integrates well with Python 3.13+ type system
- Actively maintained, widely adopted

**Alternatives Considered**:
- `argparse` (stdlib): More verbose, requires manual help text
- `click`: Good but Typer is built on click with better ergonomics
- `fire`: Auto-generates CLI but less control over help text

#### Data Model: Dataclasses

**Decision**: Use `@dataclass` with frozen=False for Task
**Rationale**:
- Native Python 3.13+ support
- Automatic `__init__`, `__repr__`, `__eq__`
- Type hints enforced at definition time
- Mutable for in-memory updates (frozen=False)

**Alternatives Considered**:
- Pydantic: Overkill for in-memory-only model
- NamedTuple: Immutable, harder to update
- Plain class: More boilerplate

#### Storage: In-Memory Dict

**Decision**: Use `dict[str, Task]` with task ID as key
**Rationale**:
- O(1) lookup by ID
- Simple iteration for list operations
- No external dependencies
- Explicit storage ownership in TaskService

**Alternatives Considered**:
- List with linear search: O(n) lookup
- SQLite in-memory: Unnecessary complexity for MVP

#### ID Generation: Sequential Counter

**Decision**: Class-level counter with T### format
**Rationale**:
- Simple, predictable IDs
- Zero-padded for consistent display
- Counter persists in service instance
- Deleted IDs not reused (per spec)

### Best Practices Applied

1. **Separation of Concerns**:
   - Model knows nothing about CLI or storage
   - Service handles business logic and storage
   - CLI handles input/output formatting

2. **Error Handling**:
   - Custom exception classes for domain errors
   - CLI catches and formats errors to stderr

3. **Testing Strategy**:
   - Unit tests for model validation
   - Unit tests for service operations
   - Integration tests for CLI commands

---

## Phase 1: Design Artifacts

### Data Model (see data-model.md)

Core entity: **Task**
- Immutable: id, created_at
- Mutable: title, description, completed

### CLI Contracts (see contracts/)

7 commands defined with exact input/output contracts:
- `todo add` - Creates task
- `todo list` - Lists all tasks
- `todo view` - Shows task details
- `todo update` - Modifies task
- `todo delete` - Removes task
- `todo complete` - Marks complete
- `todo incomplete` - Marks incomplete

### Quickstart (see quickstart.md)

Step-by-step guide to:
1. Install dependencies with UV
2. Run the CLI
3. Execute sample commands
4. Verify outputs

---

## Implementation Strategy

### Order of Implementation

1. **Phase 1: Setup** (T001-T003)
   - Project structure, pyproject.toml, UV setup

2. **Phase 2: Foundation** (T004-T008)
   - Task model, TaskService, ID generator, validators
   - Exception classes

3. **Phase 3: User Story 1 - Add Task** (T009-T012)
   - `todo add` command implementation
   - Tests for add scenarios

4. **Phase 4: User Story 2 - View Tasks** (T013-T016)
   - `todo list` command with filters
   - Tests for list scenarios

5. **Phase 5: User Story 3-7** (T017-T028)
   - Remaining commands in priority order
   - Complete/incomplete, update, delete, view single

6. **Phase 6: Polish** (T029-T032)
   - Help text, error formatting, final validation

### Parallel Opportunities

- Models and validators can be developed in parallel (Phase 2)
- Unit tests can be written in parallel with implementation
- Different user stories are independent after foundation

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Typer doesn't meet output format needs | Low | Medium | Fallback to click/argparse |
| Python 3.13 specific features unavailable | Low | Low | Target 3.12+ compatible code |
| Test coverage gaps | Medium | Medium | Write tests before implementation (TDD) |

---

## Definition of Done

- [ ] All source files generated from spec
- [ ] pytest passes with >90% coverage
- [ ] All acceptance scenarios from spec verified
- [ ] CLI help text matches command reference
- [ ] Error messages match spec exactly
- [ ] Sample session from spec runs successfully
