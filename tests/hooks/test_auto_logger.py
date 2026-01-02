"""Tests for auto_logger.py hook."""
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tests.utils import import_hook


class TestFindLatestTodoDir:
    """Unit tests for find_latest_todo_dir function."""

    @pytest.fixture
    def module(self, hooks_dir):
        return import_hook(hooks_dir / "auto_logger.py")

    def test_returns_none_when_no_todo_dir(self, module, tmp_path, monkeypatch):
        """Should return None when no TODO directory exists."""
        monkeypatch.chdir(tmp_path)
        assert module.find_latest_todo_dir() is None

    def test_returns_latest_dir(self, module, tmp_path, monkeypatch):
        """Should return the most recently modified TODO directory."""
        monkeypatch.chdir(tmp_path)

        # Create two directories with time gap
        old_dir = tmp_path / "TODO" / "old-feature"
        old_dir.mkdir(parents=True)
        time.sleep(0.1)

        new_dir = tmp_path / "TODO" / "new-feature"
        new_dir.mkdir(parents=True)

        result = module.find_latest_todo_dir()
        assert result is not None
        assert "new-feature" in result

    def test_returns_single_dir(self, module, tmp_path, monkeypatch):
        """Should return the only TODO directory when single exists."""
        monkeypatch.chdir(tmp_path)
        only_dir = tmp_path / "TODO" / "only-feature"
        only_dir.mkdir(parents=True)

        result = module.find_latest_todo_dir()
        assert "only-feature" in result


class TestAutoLoggerIntegration:
    """Integration tests for auto_logger hook."""

    @pytest.fixture
    def hook_path(self, hooks_dir):
        return hooks_dir / "auto_logger.py"

    def test_always_exits_zero(self, hook_path, tmp_path, monkeypatch):
        """Should always exit 0, even with no TODO directory."""
        monkeypatch.chdir(tmp_path)
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="",
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode == 0

    def test_appends_to_progress_file(self, hook_path, mock_todo_dir, monkeypatch):
        """Should append log entry to progress.md."""
        monkeypatch.chdir(mock_todo_dir.parent.parent)
        progress_path = mock_todo_dir / "progress.md"
        original_content = progress_path.read_text()

        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="",
            capture_output=True,
            text=True,
            cwd=mock_todo_dir.parent.parent,
        )

        assert result.returncode == 0
        new_content = progress_path.read_text()
        assert len(new_content) > len(original_content)
        assert "Auto-logged" in new_content

    def test_no_progress_file_exits_zero(self, hook_path, tmp_path, monkeypatch):
        """Should exit 0 when progress.md doesn't exist."""
        monkeypatch.chdir(tmp_path)
        todo = tmp_path / "TODO" / "feature"
        todo.mkdir(parents=True)
        # No progress.md created

        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="",
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode == 0

    def test_handles_stdin_without_blocking(self, hook_path, tmp_path, monkeypatch):
        """Should handle stdin input without blocking."""
        monkeypatch.chdir(tmp_path)
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input='{"tool": "Edit", "result": "success"}',
            capture_output=True,
            text=True,
            timeout=5,  # Should not timeout
            cwd=tmp_path,
        )
        assert result.returncode == 0
