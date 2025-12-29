"""Shared test fixtures for the Todo application tests.

This module provides pytest fixtures that can be used across all test files.
"""

import pytest
from datetime import datetime

from src.models.task import Task
from src.services.task_service import TaskService


@pytest.fixture
def task_service() -> TaskService:
    """Create a fresh TaskService instance for each test.

    Returns:
        A new TaskService with empty storage.
    """
    return TaskService()


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task for testing.

    Returns:
        A Task with ID T001, title "Buy groceries", etc.
    """
    return Task(
        id="T001",
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False,
        created_at=datetime(2025, 12, 29, 10, 30, 0),
    )


@pytest.fixture
def completed_task() -> Task:
    """Create a completed task for testing.

    Returns:
        A Task with completed=True.
    """
    return Task(
        id="T002",
        title="Call mom",
        description="",
        completed=True,
        created_at=datetime(2025, 12, 29, 10, 35, 0),
    )


@pytest.fixture
def service_with_tasks(task_service: TaskService) -> TaskService:
    """Create a TaskService with pre-populated tasks.

    Returns:
        A TaskService with 3 tasks (T001, T002, T003).
    """
    task_service.add("Buy groceries", "Milk, eggs, bread")
    task_service.add("Call mom", "")
    task_service.add("Pay bills", "Electric and water")
    # Mark T002 as complete
    task_service.mark_complete("T002")
    return task_service
