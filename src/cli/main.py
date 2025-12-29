"""Command-line interface for the Todo application.

This module defines all CLI commands using Typer. Commands interact
with TaskService for all business logic.
"""

import sys
from typing import Optional

import typer

from src import __version__
from src.services.task_service import TaskService
from src.lib.exceptions import (
    TodoError,
    TaskNotFoundError,
    EmptyTitleError,
    TitleTooLongError,
    DescriptionTooLongError,
    InvalidIDFormatError,
    NoChangesSpecifiedError,
)


# Create the Typer app
app = typer.Typer(
    name="todo",
    help="The Evolution of Todo - CLI Task Manager",
    add_completion=False,
    invoke_without_command=True,
)

# Global task service instance (in-memory storage)
_service: TaskService | None = None


def get_service() -> TaskService:
    """Get or create the global TaskService instance."""
    global _service
    if _service is None:
        _service = TaskService()
    return _service


def print_error(message: str) -> None:
    """Print an error message to stderr."""
    typer.echo(f"Error: {message}", err=True)


def version_callback(value: bool) -> None:
    """Handle --version flag."""
    if value:
        typer.echo(f"todo, version {__version__}")
        raise typer.Exit()


def show_help_guide() -> None:
    """Display a helpful command guide."""
    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("  THE EVOLUTION OF TODO - Command Guide")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo("AVAILABLE COMMANDS:")
    typer.echo("")
    typer.echo("  add         Create a new task")
    typer.echo("              Usage: todo add \"Task title\" [-d \"Description\"]")
    typer.echo("              Example: todo add \"Buy groceries\" -d \"Milk, eggs\"")
    typer.echo("")
    typer.echo("  list        Show all tasks")
    typer.echo("              Usage: todo list [--filter pending|completed]")
    typer.echo("              Example: todo list --filter pending")
    typer.echo("")
    typer.echo("  view        View task details")
    typer.echo("              Usage: todo view <task_id>")
    typer.echo("              Example: todo view T001")
    typer.echo("")
    typer.echo("  update      Update a task's title or description")
    typer.echo("              Usage: todo update <task_id> [--title \"New\"] [--description \"New\"]")
    typer.echo("              Example: todo update T001 --title \"New title\"")
    typer.echo("")
    typer.echo("  delete      Delete a task")
    typer.echo("              Usage: todo delete <task_id>")
    typer.echo("              Example: todo delete T001")
    typer.echo("")
    typer.echo("  complete    Mark a task as done")
    typer.echo("              Usage: todo complete <task_id>")
    typer.echo("              Example: todo complete T001")
    typer.echo("")
    typer.echo("  incomplete  Reopen a completed task")
    typer.echo("              Usage: todo incomplete <task_id>")
    typer.echo("              Example: todo incomplete T001")
    typer.echo("")
    typer.echo("-" * 50)
    typer.echo("OPTIONS:")
    typer.echo("  --version, -v    Show app version")
    typer.echo("  --help           Show this help message")
    typer.echo("-" * 50)
    typer.echo("")
    typer.echo("QUICK START:")
    typer.echo("  1. todo add \"My first task\"    # Create a task")
    typer.echo("  2. todo list                   # See all tasks")
    typer.echo("  3. todo complete T001          # Mark it done")
    typer.echo("")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """The Evolution of Todo - CLI Task Manager."""
    # Show help guide when no command is provided
    if ctx.invoked_subcommand is None:
        show_help_guide()


# ============================================================
# Add Command
# ============================================================

@app.command()
def add(
    title: str = typer.Argument(
        ...,
        help="The task title (required).",
    ),
    description: str = typer.Option(
        "",
        "--description",
        "-d",
        help="The task description (optional).",
    ),
) -> None:
    """Create a new task.

    Example:
        todo add "Buy groceries" --description "Milk, eggs, bread"
    """
    service = get_service()

    try:
        task = service.add(title, description)
        typer.echo(f'Task {task.id} created: "{task.title}"')
    except EmptyTitleError:
        print_error("Task title cannot be empty")
        raise typer.Exit(1)
    except TitleTooLongError:
        print_error("Title cannot exceed 200 characters")
        raise typer.Exit(1)
    except DescriptionTooLongError:
        print_error("Description cannot exceed 1000 characters")
        raise typer.Exit(1)


# ============================================================
# List Command
# ============================================================

@app.command("list")
def list_tasks(
    filter: Optional[str] = typer.Option(
        None,
        "--filter",
        "-f",
        help="Filter tasks: 'pending' or 'completed'.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-V",
        help="Show detailed output with descriptions.",
    ),
) -> None:
    """List all tasks.

    Example:
        todo list
        todo list --filter pending
        todo list --verbose
    """
    service = get_service()

    # Get tasks based on filter
    if filter == "pending":
        tasks = service.list_pending()
        count_label = f"{len(tasks)} pending"
    elif filter == "completed":
        tasks = service.list_completed()
        count_label = f"{len(tasks)} completed"
    else:
        tasks = service.list_all()
        count_label = f"{len(tasks)} total"

    # Handle empty list
    if not tasks:
        if filter is None:
            typer.echo("No tasks found. Use 'todo add <title>' to create one.")
        else:
            typer.echo(f"No {filter} tasks found.")
        return

    # Print header
    typer.echo(f"Tasks ({count_label}):")

    # Print each task
    for task in tasks:
        typer.echo(f"{task.checkbox_display()} {task.id}: {task.title}")
        if verbose:
            desc = task.description if task.description else "-"
            typer.echo(f"    Description: {desc}")
            typer.echo(f"    Created: {task.format_created_at()}")


# ============================================================
# View Command
# ============================================================

@app.command()
def view(
    task_id: str = typer.Argument(
        ...,
        help="The task ID to view (e.g., T001).",
    ),
) -> None:
    """View a task's details.

    Example:
        todo view T001
    """
    service = get_service()

    try:
        task = service.get(task_id)
        typer.echo(f"Task {task.id}")
        typer.echo(f"Title: {task.title}")
        typer.echo(f"Description: {task.description if task.description else '-'}")
        typer.echo(f"Status: {task.status_display()}")
        typer.echo(f"Created: {task.format_created_at()}")
    except InvalidIDFormatError:
        print_error("Invalid task ID format. Expected format: T###")
        raise typer.Exit(1)
    except TaskNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)


# ============================================================
# Update Command
# ============================================================

@app.command()
def update(
    task_id: str = typer.Argument(
        ...,
        help="The task ID to update (e.g., T001).",
    ),
    title: Optional[str] = typer.Option(
        None,
        "--title",
        "-t",
        help="New title for the task.",
    ),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        "-d",
        help="New description for the task.",
    ),
) -> None:
    """Update a task's title and/or description.

    Example:
        todo update T001 --title "New title"
        todo update T001 --description "New description"
    """
    service = get_service()

    try:
        task = service.update(task_id, title=title, description=description)
        typer.echo(f'Task {task.id} updated: "{task.title}"')
    except InvalidIDFormatError:
        print_error("Invalid task ID format. Expected format: T###")
        raise typer.Exit(1)
    except TaskNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)
    except NoChangesSpecifiedError:
        print_error("No changes specified. Use --title or --description")
        raise typer.Exit(1)
    except EmptyTitleError:
        print_error("Task title cannot be empty")
        raise typer.Exit(1)
    except TitleTooLongError:
        print_error("Title cannot exceed 200 characters")
        raise typer.Exit(1)
    except DescriptionTooLongError:
        print_error("Description cannot exceed 1000 characters")
        raise typer.Exit(1)


# ============================================================
# Delete Command
# ============================================================

@app.command()
def delete(
    task_id: str = typer.Argument(
        ...,
        help="The task ID to delete (e.g., T001).",
    ),
) -> None:
    """Delete a task.

    Example:
        todo delete T001
    """
    service = get_service()

    try:
        task = service.delete(task_id)
        typer.echo(f'Task {task.id} deleted: "{task.title}"')
    except InvalidIDFormatError:
        print_error("Invalid task ID format. Expected format: T###")
        raise typer.Exit(1)
    except TaskNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)


# ============================================================
# Complete Command
# ============================================================

@app.command()
def complete(
    task_id: str = typer.Argument(
        ...,
        help="The task ID to mark complete (e.g., T001).",
    ),
) -> None:
    """Mark a task as complete.

    Example:
        todo complete T001
    """
    service = get_service()

    try:
        task, changed = service.mark_complete(task_id)
        if changed:
            typer.echo(f'Task {task.id} marked complete: "{task.title}"')
        else:
            typer.echo(f"Task {task.id} is already complete")
    except InvalidIDFormatError:
        print_error("Invalid task ID format. Expected format: T###")
        raise typer.Exit(1)
    except TaskNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)


# ============================================================
# Incomplete Command
# ============================================================

@app.command()
def incomplete(
    task_id: str = typer.Argument(
        ...,
        help="The task ID to mark incomplete (e.g., T001).",
    ),
) -> None:
    """Mark a task as incomplete.

    Example:
        todo incomplete T001
    """
    service = get_service()

    try:
        task, changed = service.mark_incomplete(task_id)
        if changed:
            typer.echo(f'Task {task.id} marked incomplete: "{task.title}"')
        else:
            typer.echo(f"Task {task.id} is already incomplete")
    except InvalidIDFormatError:
        print_error("Invalid task ID format. Expected format: T###")
        raise typer.Exit(1)
    except TaskNotFoundError as e:
        print_error(str(e))
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
