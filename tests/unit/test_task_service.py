"""Unit tests for TaskService.

Tests all CRUD and state operations on the TaskService.
"""

import pytest

from src.services.task_service import TaskService
from src.lib.exceptions import (
    TaskNotFoundError,
    EmptyTitleError,
    TitleTooLongError,
    DescriptionTooLongError,
    InvalidIDFormatError,
    NoChangesSpecifiedError,
)


class TestTaskServiceAdd:
    """Tests for TaskService.add() method."""

    def test_add_task_with_title_only(self, task_service: TaskService):
        """Test adding a task with only a title."""
        task = task_service.add("Buy groceries")

        assert task.id == "T001"
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.completed is False
        assert task.created_at is not None

    def test_add_task_with_description(self, task_service: TaskService):
        """Test adding a task with title and description."""
        task = task_service.add("Buy groceries", "Milk, eggs, bread")

        assert task.id == "T001"
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"

    def test_add_multiple_tasks_sequential_ids(self, task_service: TaskService):
        """Test that task IDs are sequential."""
        task1 = task_service.add("Task 1")
        task2 = task_service.add("Task 2")
        task3 = task_service.add("Task 3")

        assert task1.id == "T001"
        assert task2.id == "T002"
        assert task3.id == "T003"

    def test_add_task_trims_whitespace(self, task_service: TaskService):
        """Test that title whitespace is trimmed."""
        task = task_service.add("  Buy groceries  ")

        assert task.title == "Buy groceries"

    def test_add_task_empty_title_raises_error(self, task_service: TaskService):
        """Test that empty title raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            task_service.add("")

    def test_add_task_whitespace_title_raises_error(self, task_service: TaskService):
        """Test that whitespace-only title raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            task_service.add("   ")

    def test_add_task_title_too_long_raises_error(self, task_service: TaskService):
        """Test that title > 200 chars raises TitleTooLongError."""
        long_title = "x" * 201
        with pytest.raises(TitleTooLongError):
            task_service.add(long_title)

    def test_add_task_title_exactly_200_chars_succeeds(self, task_service: TaskService):
        """Test that title of exactly 200 chars is allowed."""
        title = "x" * 200
        task = task_service.add(title)
        assert len(task.title) == 200

    def test_add_task_description_too_long_raises_error(self, task_service: TaskService):
        """Test that description > 1000 chars raises DescriptionTooLongError."""
        long_desc = "x" * 1001
        with pytest.raises(DescriptionTooLongError):
            task_service.add("Title", long_desc)


class TestTaskServiceGet:
    """Tests for TaskService.get() method."""

    def test_get_existing_task(self, service_with_tasks: TaskService):
        """Test getting an existing task by ID."""
        task = service_with_tasks.get("T001")

        assert task.id == "T001"
        assert task.title == "Buy groceries"

    def test_get_task_case_insensitive(self, service_with_tasks: TaskService):
        """Test that task ID lookup is case-insensitive."""
        task = service_with_tasks.get("t001")
        assert task.id == "T001"

    def test_get_nonexistent_task_raises_error(self, task_service: TaskService):
        """Test that getting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            task_service.get("T999")

        assert exc_info.value.task_id == "T999"

    def test_get_invalid_id_format_raises_error(self, task_service: TaskService):
        """Test that invalid ID format raises InvalidIDFormatError."""
        with pytest.raises(InvalidIDFormatError):
            task_service.get("abc")


class TestTaskServiceListAll:
    """Tests for TaskService.list_all() method."""

    def test_list_all_empty(self, task_service: TaskService):
        """Test listing tasks when storage is empty."""
        tasks = task_service.list_all()
        assert tasks == []

    def test_list_all_returns_all_tasks(self, service_with_tasks: TaskService):
        """Test that list_all returns all tasks."""
        tasks = service_with_tasks.list_all()
        assert len(tasks) == 3

    def test_list_all_sorted_by_id(self, service_with_tasks: TaskService):
        """Test that tasks are sorted by ID."""
        tasks = service_with_tasks.list_all()
        ids = [t.id for t in tasks]
        assert ids == ["T001", "T002", "T003"]


class TestTaskServiceListPendingCompleted:
    """Tests for list_pending() and list_completed() methods."""

    def test_list_pending_returns_incomplete_tasks(self, service_with_tasks: TaskService):
        """Test that list_pending returns only incomplete tasks."""
        tasks = service_with_tasks.list_pending()

        assert len(tasks) == 2
        assert all(not t.completed for t in tasks)

    def test_list_completed_returns_complete_tasks(self, service_with_tasks: TaskService):
        """Test that list_completed returns only complete tasks."""
        tasks = service_with_tasks.list_completed()

        assert len(tasks) == 1
        assert all(t.completed for t in tasks)


class TestTaskServiceUpdate:
    """Tests for TaskService.update() method."""

    def test_update_title(self, service_with_tasks: TaskService):
        """Test updating task title."""
        task = service_with_tasks.update("T001", title="Buy organic groceries")

        assert task.title == "Buy organic groceries"
        assert task.description == "Milk, eggs, bread"  # unchanged

    def test_update_description(self, service_with_tasks: TaskService):
        """Test updating task description."""
        task = service_with_tasks.update("T001", description="New description")

        assert task.description == "New description"
        assert task.title == "Buy groceries"  # unchanged

    def test_update_both(self, service_with_tasks: TaskService):
        """Test updating both title and description."""
        task = service_with_tasks.update(
            "T001",
            title="New title",
            description="New description"
        )

        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_no_changes_raises_error(self, service_with_tasks: TaskService):
        """Test that update without changes raises NoChangesSpecifiedError."""
        with pytest.raises(NoChangesSpecifiedError):
            service_with_tasks.update("T001")

    def test_update_nonexistent_raises_error(self, task_service: TaskService):
        """Test that updating non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            task_service.update("T999", title="New")

    def test_update_empty_title_raises_error(self, service_with_tasks: TaskService):
        """Test that empty title in update raises EmptyTitleError."""
        with pytest.raises(EmptyTitleError):
            service_with_tasks.update("T001", title="")


class TestTaskServiceDelete:
    """Tests for TaskService.delete() method."""

    def test_delete_existing_task(self, service_with_tasks: TaskService):
        """Test deleting an existing task."""
        task = service_with_tasks.delete("T002")

        assert task.id == "T002"
        assert service_with_tasks.count() == 2
        with pytest.raises(TaskNotFoundError):
            service_with_tasks.get("T002")

    def test_delete_preserves_other_ids(self, service_with_tasks: TaskService):
        """Test that deleting doesn't renumber other IDs."""
        service_with_tasks.delete("T002")

        # T001 and T003 should still exist
        assert service_with_tasks.get("T001").id == "T001"
        assert service_with_tasks.get("T003").id == "T003"

    def test_delete_nonexistent_raises_error(self, task_service: TaskService):
        """Test that deleting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            task_service.delete("T999")


class TestTaskServiceMarkComplete:
    """Tests for TaskService.mark_complete() method."""

    def test_mark_complete_incomplete_task(self, service_with_tasks: TaskService):
        """Test marking an incomplete task as complete."""
        task, changed = service_with_tasks.mark_complete("T001")

        assert task.completed is True
        assert changed is True

    def test_mark_complete_already_complete(self, service_with_tasks: TaskService):
        """Test marking an already complete task."""
        task, changed = service_with_tasks.mark_complete("T002")

        assert task.completed is True
        assert changed is False

    def test_mark_complete_nonexistent_raises_error(self, task_service: TaskService):
        """Test that marking non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            task_service.mark_complete("T999")


class TestTaskServiceMarkIncomplete:
    """Tests for TaskService.mark_incomplete() method."""

    def test_mark_incomplete_complete_task(self, service_with_tasks: TaskService):
        """Test marking a complete task as incomplete."""
        task, changed = service_with_tasks.mark_incomplete("T002")

        assert task.completed is False
        assert changed is True

    def test_mark_incomplete_already_incomplete(self, service_with_tasks: TaskService):
        """Test marking an already incomplete task."""
        task, changed = service_with_tasks.mark_incomplete("T001")

        assert task.completed is False
        assert changed is False

    def test_mark_incomplete_nonexistent_raises_error(self, task_service: TaskService):
        """Test that marking non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            task_service.mark_incomplete("T999")
