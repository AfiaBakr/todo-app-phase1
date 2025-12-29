# Tasks: Core Todo Operations

**Input**: Design documents from `/specs/core-todo-operations/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md, quickstart.md

**Tests**: Tests are OPTIONAL. This task list includes tests as the spec defines acceptance criteria (SC-004: >90% coverage).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md (src/models/, src/services/, src/cli/, src/lib/, tests/)
- [x] T002 Create pyproject.toml with Python 3.13+, typer, pytest dependencies
- [x] T003 [P] Create all __init__.py files for package structure
- [ ] T004 [P] Configure UV package manager and create virtual environment

**Checkpoint**: Project structure ready, dependencies installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Create exception classes (TodoError, TaskNotFoundError, ValidationError, etc.) in src/lib/exceptions.py
- [x] T006 [P] Implement IDGenerator class in src/lib/id_generator.py
- [x] T007 [P] Implement validators (validate_title, validate_description, validate_task_id) in src/lib/validators.py
- [x] T008 Create Task dataclass with all fields in src/models/task.py
- [x] T009 Create TaskService class skeleton with __init__ in src/services/task_service.py
- [x] T010 Create Typer app skeleton with --help and --version in src/cli/main.py
- [x] T011 [P] Create test fixtures (task_service fixture, sample tasks) in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1)

**Goal**: Users can create new tasks with title and optional description

**Independent Test**: Run `todo add "My task"` and verify task appears with unique ID

### Tests for User Story 1

- [x] T012 [P] [US1] Write unit tests for TaskService.add() in tests/unit/test_task_service.py
- [x] T013 [P] [US1] Write unit tests for title/description validation in tests/unit/test_validators.py
- [x] T014 [P] [US1] Write CLI contract tests for `todo add` output format in tests/contract/test_cli_contracts.py

### Implementation for User Story 1

- [x] T015 [US1] Implement TaskService.add() method in src/services/task_service.py
- [x] T016 [US1] Implement `todo add` command with --description option in src/cli/main.py
- [x] T017 [US1] Add error handling for empty title, title too long in src/cli/main.py
- [x] T018 [US1] Verify all US1 acceptance scenarios pass

**Checkpoint**: User Story 1 complete - can add tasks independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can view all tasks with completion status indicators

**Independent Test**: Add tasks, run `todo list` to verify display format

### Tests for User Story 2

- [x] T019 [P] [US2] Write unit tests for TaskService.list_all(), list_pending(), list_completed() in tests/unit/test_task_service.py
- [x] T020 [P] [US2] Write CLI contract tests for `todo list` output format in tests/contract/test_cli_contracts.py

### Implementation for User Story 2

- [x] T021 [US2] Implement TaskService.list_all() method in src/services/task_service.py
- [x] T022 [US2] Implement TaskService.list_pending() and list_completed() methods in src/services/task_service.py
- [x] T023 [US2] Implement `todo list` command with --filter and --verbose options in src/cli/main.py
- [x] T024 [US2] Format output with [ ]/[x] status indicators in src/cli/main.py
- [x] T025 [US2] Handle empty list case with helpful message in src/cli/main.py
- [x] T026 [US2] Verify all US2 acceptance scenarios pass

**Checkpoint**: User Stories 1 AND 2 complete - can add and list tasks

---

## Phase 5: User Story 6 - Mark Task Complete (Priority: P1)

**Goal**: Users can mark tasks as complete to track progress

**Independent Test**: Add task, run `todo complete T001`, verify [x] status in list

### Tests for User Story 6

- [x] T027 [P] [US6] Write unit tests for TaskService.mark_complete() in tests/unit/test_task_service.py
- [x] T028 [P] [US6] Write CLI contract tests for `todo complete` output in tests/contract/test_cli_contracts.py

### Implementation for User Story 6

- [x] T029 [US6] Implement TaskService.mark_complete() returning (Task, changed: bool) in src/services/task_service.py
- [x] T030 [US6] Implement `todo complete` command in src/cli/main.py
- [x] T031 [US6] Handle idempotent case (already complete) with appropriate message in src/cli/main.py
- [x] T032 [US6] Handle task not found error in src/cli/main.py
- [x] T033 [US6] Verify all US6 acceptance scenarios pass

**Checkpoint**: P1 user stories complete - MVP functional (add, list, complete)

---

## Phase 6: User Story 3 - View Single Task (Priority: P2)

**Goal**: Users can view full details of a specific task by ID

**Independent Test**: Add task, run `todo view T001` to see all fields

### Tests for User Story 3

- [x] T034 [P] [US3] Write unit tests for TaskService.get() in tests/unit/test_task_service.py
- [x] T035 [P] [US3] Write CLI contract tests for `todo view` output in tests/contract/test_cli_contracts.py

### Implementation for User Story 3

- [x] T036 [US3] Implement TaskService.get() method in src/services/task_service.py
- [x] T037 [US3] Implement `todo view` command in src/cli/main.py
- [x] T038 [US3] Format detailed output (Title, Description, Status, Created) in src/cli/main.py
- [x] T039 [US3] Handle task not found and missing ID errors in src/cli/main.py
- [x] T040 [US3] Verify all US3 acceptance scenarios pass

**Checkpoint**: User Story 3 complete

---

## Phase 7: User Story 4 - Update a Task (Priority: P2)

**Goal**: Users can update task title and/or description

**Independent Test**: Add task, update title, view to confirm change

### Tests for User Story 4

- [x] T041 [P] [US4] Write unit tests for TaskService.update() in tests/unit/test_task_service.py
- [x] T042 [P] [US4] Write CLI contract tests for `todo update` output in tests/contract/test_cli_contracts.py

### Implementation for User Story 4

- [x] T043 [US4] Implement TaskService.update() method in src/services/task_service.py
- [x] T044 [US4] Implement `todo update` command with --title and --description options in src/cli/main.py
- [x] T045 [US4] Handle validation errors (empty title, too long) in src/cli/main.py
- [x] T046 [US4] Handle no changes specified error in src/cli/main.py
- [x] T047 [US4] Verify all US4 acceptance scenarios pass

**Checkpoint**: User Story 4 complete

---

## Phase 8: User Story 5 - Delete a Task (Priority: P2)

**Goal**: Users can delete tasks they no longer need

**Independent Test**: Add task, delete it, list to confirm removal

### Tests for User Story 5

- [x] T048 [P] [US5] Write unit tests for TaskService.delete() in tests/unit/test_task_service.py
- [x] T049 [P] [US5] Write CLI contract tests for `todo delete` output in tests/contract/test_cli_contracts.py

### Implementation for User Story 5

- [x] T050 [US5] Implement TaskService.delete() method in src/services/task_service.py
- [x] T051 [US5] Implement `todo delete` command in src/cli/main.py
- [x] T052 [US5] Handle task not found and missing ID errors in src/cli/main.py
- [x] T053 [US5] Verify IDs are NOT renumbered after deletion
- [x] T054 [US5] Verify all US5 acceptance scenarios pass

**Checkpoint**: User Story 5 complete

---

## Phase 9: User Story 7 - Mark Task Incomplete (Priority: P2)

**Goal**: Users can reopen completed tasks

**Independent Test**: Complete a task, mark incomplete, verify [ ] status

### Tests for User Story 7

- [x] T055 [P] [US7] Write unit tests for TaskService.mark_incomplete() in tests/unit/test_task_service.py
- [x] T056 [P] [US7] Write CLI contract tests for `todo incomplete` output in tests/contract/test_cli_contracts.py

### Implementation for User Story 7

- [x] T057 [US7] Implement TaskService.mark_incomplete() returning (Task, changed: bool) in src/services/task_service.py
- [x] T058 [US7] Implement `todo incomplete` command in src/cli/main.py
- [x] T059 [US7] Handle idempotent case (already incomplete) with appropriate message in src/cli/main.py
- [x] T060 [US7] Verify all US7 acceptance scenarios pass

**Checkpoint**: All user stories complete

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T061 [P] Verify all CLI help text matches command reference in spec
- [x] T062 [P] Verify all error messages match spec exactly
- [x] T063 [P] Run full test suite and verify >90% coverage
- [x] T064 [P] Run sample session from spec and verify all outputs match
- [x] T065 Validate ID case-insensitivity across all commands
- [x] T066 Final code review against constitution principles

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ──────────────────────────────────────────────────┐
                                                                  │
Phase 2: Foundational ◄──────────────────────────────────────────┘
         │
         │ (BLOCKS all user stories)
         ▼
┌────────────────────────────────────────────────────────────────┐
│ User Stories (can run in parallel after Phase 2)               │
│                                                                │
│  Phase 3: US1 Add ─────┐                                       │
│  Phase 4: US2 List ────┼──► MVP Complete                       │
│  Phase 5: US6 Complete ┘                                       │
│                                                                │
│  Phase 6: US3 View ────┐                                       │
│  Phase 7: US4 Update ──┼──► Full Feature Set                   │
│  Phase 8: US5 Delete ──┤                                       │
│  Phase 9: US7 Incomplete┘                                      │
└────────────────────────────────────────────────────────────────┘
         │
         ▼
Phase 10: Polish
```

### User Story Dependencies

| User Story | Depends On | Can Parallel With |
|------------|------------|-------------------|
| US1 (Add) | Phase 2 | US2, US6 |
| US2 (List) | Phase 2 | US1, US6 |
| US6 (Complete) | Phase 2 | US1, US2 |
| US3 (View) | Phase 2 | US4, US5, US7 |
| US4 (Update) | Phase 2 | US3, US5, US7 |
| US5 (Delete) | Phase 2 | US3, US4, US7 |
| US7 (Incomplete) | Phase 2 | US3, US4, US5 |

### Within Each User Story

1. Tests MUST be written and FAIL before implementation
2. Service methods before CLI commands
3. Core implementation before error handling
4. Verify acceptance scenarios before moving on

---

## Parallel Execution Examples

### Phase 2: Foundational (All [P] tasks)

```bash
# Launch these tasks in parallel:
Task: "Create exception classes in src/lib/exceptions.py"
Task: "Implement IDGenerator in src/lib/id_generator.py"
Task: "Implement validators in src/lib/validators.py"
Task: "Create test fixtures in tests/conftest.py"
```

### Phase 3: User Story 1 (Tests in parallel)

```bash
# Launch test tasks in parallel:
Task: "Write unit tests for TaskService.add()"
Task: "Write unit tests for title/description validation"
Task: "Write CLI contract tests for todo add"

# Then implementation sequentially:
Task: "Implement TaskService.add()"
Task: "Implement todo add command"
```

### Multiple User Stories (Team parallel)

```bash
# Developer A: User Story 1 (Add)
# Developer B: User Story 2 (List)
# Developer C: User Story 6 (Complete)
# All can work simultaneously after Phase 2
```

---

## Implementation Strategy

### MVP First (P1 User Stories Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: US1 - Add Task
4. Complete Phase 4: US2 - View Tasks
5. Complete Phase 5: US6 - Mark Complete
6. **STOP and VALIDATE**: Test MVP independently
7. Deploy/demo if ready

**MVP Scope**: 3 commands (add, list, complete) = functional todo app

### Incremental Delivery

| Milestone | User Stories | Commands Available |
|-----------|--------------|-------------------|
| MVP | US1, US2, US6 | add, list, complete |
| +View | US3 | + view |
| +Update | US4 | + update |
| +Delete | US5 | + delete |
| Full | US7 | + incomplete |

### Task Count Summary

| Phase | Task Count | Parallelizable |
|-------|------------|----------------|
| Setup | 4 | 2 |
| Foundational | 7 | 4 |
| US1 (Add) | 7 | 3 |
| US2 (List) | 8 | 2 |
| US6 (Complete) | 7 | 2 |
| US3 (View) | 7 | 2 |
| US4 (Update) | 7 | 2 |
| US5 (Delete) | 7 | 2 |
| US7 (Incomplete) | 6 | 2 |
| Polish | 6 | 4 |
| **Total** | **66** | **25** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
