"""Contract tests for CLI output format.

These tests verify that CLI output matches the exact format specified
in the contracts documentation.
"""

import pytest
from typer.testing import CliRunner
from src.cli.main import app, _service

runner = CliRunner()


@pytest.fixture(autouse=True)
def reset_service():
    """Reset the global service before each test."""
    import src.cli.main as main_module
    main_module._service = None
    yield
    main_module._service = None


class TestAddCommandContract:
    """Contract tests for 'todo add' command."""

    def test_add_success_output_format(self):
        """Test that add success output matches contract."""
        result = runner.invoke(app, ["add", "Buy groceries"])

        assert result.exit_code == 0
        assert result.output.strip() == 'Task T001 created: "Buy groceries"'

    def test_add_with_description_output(self):
        """Test add with description output format."""
        result = runner.invoke(
            app,
            ["add", "Buy groceries", "--description", "Milk, eggs"]
        )

        assert result.exit_code == 0
        assert result.output.strip() == 'Task T001 created: "Buy groceries"'

    def test_add_empty_title_error(self):
        """Test add empty title error output."""
        result = runner.invoke(app, ["add", ""])

        assert result.exit_code == 1
        assert "Error: Task title cannot be empty" in result.output

    def test_add_title_too_long_error(self):
        """Test add title too long error output."""
        long_title = "x" * 201
        result = runner.invoke(app, ["add", long_title])

        assert result.exit_code == 1
        assert "Error: Title cannot exceed 200 characters" in result.output


class TestListCommandContract:
    """Contract tests for 'todo list' command."""

    def test_list_empty_output(self):
        """Test list empty output format."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No tasks found. Use 'todo add <title>' to create one." in result.output

    def test_list_with_tasks_output_format(self):
        """Test list with tasks output format."""
        # Add tasks first
        runner.invoke(app, ["add", "Buy groceries"])
        runner.invoke(app, ["add", "Call mom"])

        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Tasks (2 total):" in result.output
        assert "[ ] T001: Buy groceries" in result.output
        assert "[ ] T002: Call mom" in result.output

    def test_list_with_complete_task_shows_checkbox(self):
        """Test that completed tasks show [x] checkbox."""
        runner.invoke(app, ["add", "Buy groceries"])
        runner.invoke(app, ["complete", "T001"])

        result = runner.invoke(app, ["list"])

        assert "[x] T001: Buy groceries" in result.output

    def test_list_filter_pending_output(self):
        """Test list filter pending output format."""
        runner.invoke(app, ["add", "Buy groceries"])
        runner.invoke(app, ["add", "Call mom"])
        runner.invoke(app, ["complete", "T001"])

        result = runner.invoke(app, ["list", "--filter", "pending"])

        assert result.exit_code == 0
        assert "Tasks (1 pending):" in result.output
        assert "[ ] T002: Call mom" in result.output
        assert "T001" not in result.output

    def test_list_filter_completed_output(self):
        """Test list filter completed output format."""
        runner.invoke(app, ["add", "Buy groceries"])
        runner.invoke(app, ["complete", "T001"])

        result = runner.invoke(app, ["list", "--filter", "completed"])

        assert result.exit_code == 0
        assert "Tasks (1 completed):" in result.output
        assert "[x] T001: Buy groceries" in result.output


class TestViewCommandContract:
    """Contract tests for 'todo view' command."""

    def test_view_task_output_format(self):
        """Test view task output format."""
        runner.invoke(app, ["add", "Buy groceries", "--description", "Milk, eggs"])

        result = runner.invoke(app, ["view", "T001"])

        assert result.exit_code == 0
        assert "Task T001" in result.output
        assert "Title: Buy groceries" in result.output
        assert "Description: Milk, eggs" in result.output
        assert "Status: Pending" in result.output
        assert "Created:" in result.output

    def test_view_complete_task_status(self):
        """Test that completed task shows Complete status."""
        runner.invoke(app, ["add", "Buy groceries"])
        runner.invoke(app, ["complete", "T001"])

        result = runner.invoke(app, ["view", "T001"])

        assert "Status: Complete" in result.output

    def test_view_not_found_error(self):
        """Test view not found error output."""
        result = runner.invoke(app, ["view", "T999"])

        assert result.exit_code == 1
        assert "Error: Task T999 not found" in result.output

    def test_view_invalid_id_error(self):
        """Test view invalid ID error output."""
        result = runner.invoke(app, ["view", "abc"])

        assert result.exit_code == 1
        assert "Error: Invalid task ID format. Expected format: T###" in result.output


class TestUpdateCommandContract:
    """Contract tests for 'todo update' command."""

    def test_update_title_output(self):
        """Test update title output format."""
        runner.invoke(app, ["add", "Buy groceries"])

        result = runner.invoke(app, ["update", "T001", "--title", "Buy organic"])

        assert result.exit_code == 0
        assert 'Task T001 updated: "Buy organic"' in result.output

    def test_update_not_found_error(self):
        """Test update not found error output."""
        result = runner.invoke(app, ["update", "T999", "--title", "New"])

        assert result.exit_code == 1
        assert "Error: Task T999 not found" in result.output

    def test_update_no_changes_error(self):
        """Test update no changes error output."""
        runner.invoke(app, ["add", "Buy groceries"])

        result = runner.invoke(app, ["update", "T001"])

        assert result.exit_code == 1
        assert "Error: No changes specified. Use --title or --description" in result.output


class TestDeleteCommandContract:
    """Contract tests for 'todo delete' command."""

    def test_delete_success_output(self):
        """Test delete success output format."""
        runner.invoke(app, ["add", "Buy groceries"])

        result = runner.invoke(app, ["delete", "T001"])

        assert result.exit_code == 0
        assert 'Task T001 deleted: "Buy groceries"' in result.output

    def test_delete_not_found_error(self):
        """Test delete not found error output."""
        result = runner.invoke(app, ["delete", "T999"])

        assert result.exit_code == 1
        assert "Error: Task T999 not found" in result.output


class TestCompleteCommandContract:
    """Contract tests for 'todo complete' command."""

    def test_complete_success_output(self):
        """Test complete success output format."""
        runner.invoke(app, ["add", "Buy groceries"])

        result = runner.invoke(app, ["complete", "T001"])

        assert result.exit_code == 0
        assert 'Task T001 marked complete: "Buy groceries"' in result.output

    def test_complete_already_complete_output(self):
        """Test complete already complete output format."""
        runner.invoke(app, ["add", "Buy groceries"])
        runner.invoke(app, ["complete", "T001"])

        result = runner.invoke(app, ["complete", "T001"])

        assert result.exit_code == 0
        assert "Task T001 is already complete" in result.output

    def test_complete_not_found_error(self):
        """Test complete not found error output."""
        result = runner.invoke(app, ["complete", "T999"])

        assert result.exit_code == 1
        assert "Error: Task T999 not found" in result.output


class TestIncompleteCommandContract:
    """Contract tests for 'todo incomplete' command."""

    def test_incomplete_success_output(self):
        """Test incomplete success output format."""
        runner.invoke(app, ["add", "Buy groceries"])
        runner.invoke(app, ["complete", "T001"])

        result = runner.invoke(app, ["incomplete", "T001"])

        assert result.exit_code == 0
        assert 'Task T001 marked incomplete: "Buy groceries"' in result.output

    def test_incomplete_already_incomplete_output(self):
        """Test incomplete already incomplete output format."""
        runner.invoke(app, ["add", "Buy groceries"])

        result = runner.invoke(app, ["incomplete", "T001"])

        assert result.exit_code == 0
        assert "Task T001 is already incomplete" in result.output

    def test_incomplete_not_found_error(self):
        """Test incomplete not found error output."""
        result = runner.invoke(app, ["incomplete", "T999"])

        assert result.exit_code == 1
        assert "Error: Task T999 not found" in result.output


class TestVersionCommand:
    """Contract tests for --version flag."""

    def test_version_output(self):
        """Test version output format."""
        result = runner.invoke(app, ["--version"])

        assert result.exit_code == 0
        assert "todo, version 0.1.0" in result.output
