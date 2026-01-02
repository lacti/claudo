"""Shared pytest fixtures for Claudo tests."""
import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parents[1]


@pytest.fixture
def hooks_dir(project_root):
    """Return the hooks directory."""
    return project_root / ".claude" / "hooks"


@pytest.fixture
def commands_dir(project_root):
    """Return the commands directory."""
    return project_root / ".claude" / "commands"


@pytest.fixture
def mock_todo_dir(tmp_path):
    """Create a mock TODO directory structure."""
    todo = tmp_path / "TODO" / "test-feature"
    todo.mkdir(parents=True)

    (todo / "PLAN.md").write_text("# Test Plan\n")
    (todo / "progress.md").write_text("# Progress\n")
    (todo / "checklist.md").write_text("- [ ] Item 1\n- [ ] Item 2\n")
    (todo / "01.md").write_text("# Task 01\n")

    return todo


@pytest.fixture
def complete_checklist(tmp_path):
    """Create a TODO directory with all items checked."""
    todo = tmp_path / "TODO" / "complete-feature"
    todo.mkdir(parents=True)
    (todo / "checklist.md").write_text("- [x] Done 1\n- [x] Done 2\n")
    # Create session file for hooks to be active
    session_dir = tmp_path / ".claude"
    session_dir.mkdir(parents=True)
    (session_dir / ".do-session").write_text("")
    return todo


@pytest.fixture
def incomplete_checklist(tmp_path):
    """Create a TODO directory with unchecked items."""
    todo = tmp_path / "TODO" / "incomplete-feature"
    todo.mkdir(parents=True)
    (todo / "checklist.md").write_text("- [x] Done\n- [ ] Not done\n- [ ] Also not\n")
    # Create session file for hooks to be active
    session_dir = tmp_path / ".claude"
    session_dir.mkdir(parents=True)
    (session_dir / ".do-session").write_text("")
    return todo
