# Hackathon II

## The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI

The future of software development is AI-native and spec-driven. As AI agents like Claude Code become more powerful, the role of the engineer shifts from "syntax writer" to "system architect." We have already explored Spec-Driven Book Authoring. Now, we want you to master the Architecture of Intelligence.

---

## Project Details: The Evolution of Todo

| Aspect | Description |
|--------|-------------|
| **Focus and Theme** | From CLI to Distributed Cloud-Native AI Systems |
| **Goal** | Students act as Product Architects, using AI to build progressively complex software without writing boilerplate code |

---

## Project Overview

This project simulates the real-world evolution of software. You will start with a simple script and end with a Kubernetes-managed, event-driven, AI-powered distributed system.

---

## Phase I: Todo In-Memory Python Console App - Basic Level Functionality

### Objective

Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.

### Requirements

- Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
- Use spec-driven development with Claude Code and Spec-Kit Plus
- Follow clean code principles and proper Python project structure

### Technology Stack

- UV
- Python 3.13+
- Claude Code
- Spec-Kit Plus

---

## Deliverables

### 1. GitHub Repository Structure

```
todo_phase1/
├── .specify/memory/constitution.md    # Constitution file
├── specs/                             # Specification files
├── history/                           # Specs history folder
├── src/                               # Python source code
│   ├── cli/main.py                    # CLI entry point
│   ├── models/task.py                 # Task model
│   ├── services/task_service.py       # Business logic
│   └── lib/                           # Utilities
├── tests/                             # Test files
├── README.md                          # Setup instructions
├── CLAUDE.md                          # Claude Code instructions
└── pyproject.toml                     # Project configuration
```

### 2. Working Console Application Features

| Command | Description | Example |
|---------|-------------|---------|
| `todo add` | Add tasks with title and description | `todo add "Buy groceries" -d "Milk, eggs"` |
| `todo list` | List all tasks with status indicators | `todo list --filter pending` |
| `todo view` | View task details | `todo view T001` |
| `todo update` | Update task details | `todo update T001 --title "New title"` |
| `todo delete` | Delete tasks by ID | `todo delete T001` |
| `todo complete` | Mark tasks as complete | `todo complete T001` |
| `todo incomplete` | Mark tasks as incomplete | `todo incomplete T001` |

---

## Installation & Setup

### Prerequisites

- Python 3.13+
- UV package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/AfiaBakr/todo-app-phase1.git
cd todo-app-phase1

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Running the Application

```bash
# Using UV (recommended)
uv run todo

# Or activate virtual environment first
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac

# Then run directly
todo
```

---

## Usage Examples

```bash
# Show help
todo

# Add a new task
todo add "Buy groceries" -d "Milk, eggs, bread"

# List all tasks
todo list

# List pending tasks only
todo list --filter pending

# List completed tasks only
todo list --filter completed

# View task details
todo view T001

# Update a task
todo update T001 --title "Buy vegetables"
todo update T001 --description "Updated description"

# Mark task as complete
todo complete T001

# Mark task as incomplete
todo incomplete T001

# Delete a task
todo delete T001

# Check version
todo --version
```

---

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src
```

---

## Author

**Afia Bakr**

---

## License

MIT License
