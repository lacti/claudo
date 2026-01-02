"""Tests for quality_gate.py hook."""
import subprocess
import sys
from pathlib import Path

import pytest

from tests.utils import import_hook


class TestGetSessionPhase:
    """Unit tests for get_session_phase function."""

    @pytest.fixture
    def module(self, hooks_dir):
        return import_hook(hooks_dir / "quality_gate.py")

    def test_returns_none_when_no_session(self, module, tmp_path, monkeypatch):
        """Should return None when no .do-session file exists."""
        monkeypatch.chdir(tmp_path)
        assert module.get_session_phase() is None

    def test_returns_phase_from_session(self, module, tmp_path, monkeypatch):
        """Should return phase from .do-session file."""
        session_dir = tmp_path / ".claude"
        session_dir.mkdir(parents=True)
        (session_dir / ".do-session").write_text('{"phase": "executing"}')
        monkeypatch.chdir(tmp_path)
        assert module.get_session_phase() == "executing"

    def test_returns_planning_phase(self, module, tmp_path, monkeypatch):
        """Should return planning phase from .do-session file."""
        session_dir = tmp_path / ".claude"
        session_dir.mkdir(parents=True)
        (session_dir / ".do-session").write_text('{"phase": "planning"}')
        monkeypatch.chdir(tmp_path)
        assert module.get_session_phase() == "planning"

    def test_returns_none_for_invalid_json(self, module, tmp_path, monkeypatch):
        """Should return None for invalid JSON in .do-session."""
        session_dir = tmp_path / ".claude"
        session_dir.mkdir(parents=True)
        (session_dir / ".do-session").write_text("not valid json")
        monkeypatch.chdir(tmp_path)
        assert module.get_session_phase() is None

    def test_returns_none_for_missing_phase(self, module, tmp_path, monkeypatch):
        """Should return None when phase key is missing."""
        session_dir = tmp_path / ".claude"
        session_dir.mkdir(parents=True)
        (session_dir / ".do-session").write_text('{"feature": "test"}')
        monkeypatch.chdir(tmp_path)
        assert module.get_session_phase() is None


class TestIsDoSessionActive:
    """Unit tests for is_do_session_active function."""

    @pytest.fixture
    def module(self, hooks_dir):
        return import_hook(hooks_dir / "quality_gate.py")

    def test_inactive_when_no_session(self, module, tmp_path, monkeypatch):
        """Should return False when no session file."""
        monkeypatch.chdir(tmp_path)
        assert module.is_do_session_active() is False

    def test_inactive_when_planning_phase(self, module, tmp_path, monkeypatch):
        """Should return False when phase is planning."""
        session_dir = tmp_path / ".claude"
        session_dir.mkdir(parents=True)
        (session_dir / ".do-session").write_text('{"phase": "planning"}')
        monkeypatch.chdir(tmp_path)
        assert module.is_do_session_active() is False

    def test_active_when_executing_phase(self, module, tmp_path, monkeypatch):
        """Should return True when phase is executing."""
        session_dir = tmp_path / ".claude"
        session_dir.mkdir(parents=True)
        (session_dir / ".do-session").write_text('{"phase": "executing"}')
        monkeypatch.chdir(tmp_path)
        assert module.is_do_session_active() is True


class TestFindActiveChecklist:
    """Unit tests for find_active_checklist function."""

    @pytest.fixture
    def module(self, hooks_dir):
        return import_hook(hooks_dir / "quality_gate.py")

    def test_returns_none_when_no_todo_dir(self, module, tmp_path, monkeypatch):
        """Should return None when no TODO directory exists."""
        monkeypatch.chdir(tmp_path)
        assert module.find_active_checklist() is None

    def test_returns_none_when_no_checklist(self, module, tmp_path, monkeypatch):
        """Should return None when TODO exists but no checklist.md."""
        (tmp_path / "TODO" / "feature").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        assert module.find_active_checklist() is None

    def test_returns_checklist_path(self, module, tmp_path, monkeypatch):
        """Should return checklist path when it exists."""
        todo = tmp_path / "TODO" / "feature"
        todo.mkdir(parents=True)
        checklist = todo / "checklist.md"
        checklist.write_text("- [ ] Test item")
        monkeypatch.chdir(tmp_path)

        result = module.find_active_checklist()
        assert result is not None
        assert "checklist.md" in result


class TestCheckQualityGate:
    """Unit tests for check_quality_gate function."""

    @pytest.fixture
    def module(self, hooks_dir):
        return import_hook(hooks_dir / "quality_gate.py")

    def test_all_checked_passes(self, module, tmp_path):
        """Should pass when all items are checked."""
        checklist = tmp_path / "checklist.md"
        checklist.write_text("- [x] Done 1\n- [x] Done 2\n- [x] Done 3\n")

        passed, remaining = module.check_quality_gate(str(checklist))
        assert passed is True
        assert remaining == 0

    def test_unchecked_items_fails(self, module, tmp_path):
        """Should fail when unchecked items exist."""
        checklist = tmp_path / "checklist.md"
        checklist.write_text("- [x] Done\n- [ ] Not done\n- [ ] Also not\n")

        passed, remaining = module.check_quality_gate(str(checklist))
        assert passed is False
        assert remaining == 2

    def test_empty_checklist_passes(self, module, tmp_path):
        """Empty checklist should pass."""
        checklist = tmp_path / "checklist.md"
        checklist.write_text("# Checklist\n\nNo items yet.\n")

        passed, remaining = module.check_quality_gate(str(checklist))
        assert passed is True
        assert remaining == 0

    def test_mixed_spacing_detected(self, module, tmp_path):
        """Should detect unchecked items with various spacing."""
        checklist = tmp_path / "checklist.md"
        checklist.write_text("- [x] Done\n-[ ] No space\n- [  ] Extra space\n")

        passed, remaining = module.check_quality_gate(str(checklist))
        # The regex '-\s*\[\s*\]' should match '- [ ]' and '-[ ]' but not '- [  ]'
        assert passed is False


class TestQualityGateIntegration:
    """Integration tests for quality_gate hook."""

    @pytest.fixture
    def hook_path(self, hooks_dir):
        return hooks_dir / "quality_gate.py"

    def test_no_todo_exits_zero(self, hook_path, tmp_path, monkeypatch):
        """Should exit 0 when no TODO directory."""
        monkeypatch.chdir(tmp_path)
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            capture_output=True,
            text=True,
            cwd=tmp_path,
        )
        assert result.returncode == 0

    def test_complete_checklist_exits_zero(
        self, hook_path, complete_checklist, monkeypatch
    ):
        """Should exit 0 when all items checked."""
        monkeypatch.chdir(complete_checklist.parent.parent)
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            capture_output=True,
            text=True,
            cwd=complete_checklist.parent.parent,
        )
        assert result.returncode == 0

    def test_incomplete_checklist_exits_one(
        self, hook_path, incomplete_checklist, monkeypatch
    ):
        """Should exit 1 when unchecked items exist."""
        monkeypatch.chdir(incomplete_checklist.parent.parent)
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            capture_output=True,
            text=True,
            cwd=incomplete_checklist.parent.parent,
        )
        assert result.returncode == 1
        assert "[Quality Gate]" in result.stderr
        assert "2" in result.stderr  # 2 incomplete items

    def test_incomplete_shows_stdout_message(
        self, hook_path, incomplete_checklist, monkeypatch
    ):
        """Should output message to stdout when incomplete."""
        monkeypatch.chdir(incomplete_checklist.parent.parent)
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            capture_output=True,
            text=True,
            cwd=incomplete_checklist.parent.parent,
        )
        assert "Checklist verification failed" in result.stdout

    def test_planning_phase_exits_zero(
        self, hook_path, planning_phase_checklist, monkeypatch
    ):
        """Should exit 0 when in planning phase even with incomplete items."""
        monkeypatch.chdir(planning_phase_checklist.parent.parent)
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            capture_output=True,
            text=True,
            cwd=planning_phase_checklist.parent.parent,
        )
        # Should exit 0 because phase is 'planning', not 'executing'
        assert result.returncode == 0
        assert "[Quality Gate]" not in result.stderr
