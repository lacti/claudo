"""Tests for gatekeeper.py hook."""
import subprocess
import sys
from pathlib import Path

import pytest

from tests.utils import import_hook


class TestAnalyzeComplexity:
    """Unit tests for analyze_complexity function."""

    @pytest.fixture
    def analyze_func(self, hooks_dir):
        """Import analyze_complexity from gatekeeper module."""
        module = import_hook(hooks_dir / "gatekeeper.py")
        return module.analyze_complexity

    @pytest.mark.parametrize(
        "prompt,expected",
        [
            ("fix typo", "simple"),
            ("explain this", "simple"),
            ("what is X", "simple"),
            ("show me", "simple"),
            ("list files", "simple"),
        ],
    )
    def test_simple_prompts(self, analyze_func, prompt, expected):
        """Short prompts with simple keywords should return 'simple'."""
        assert analyze_func(prompt) == expected

    @pytest.mark.parametrize(
        "prompt,expected",
        [
            ("implement authentication system", "complex"),
            ("create a new user management feature", "complex"),
            ("build the entire frontend", "complex"),
            ("refactor the database layer", "complex"),
            ("design the API architecture", "complex"),
        ],
    )
    def test_complex_prompts_by_keyword(self, analyze_func, prompt, expected):
        """Prompts with complex keywords should return 'complex'."""
        assert analyze_func(prompt) == expected

    def test_long_prompt_is_complex(self, analyze_func):
        """Prompts longer than 50 characters should be 'complex'."""
        long_prompt = "a" * 51
        assert analyze_func(long_prompt) == "complex"

    @pytest.mark.parametrize(
        "prompt",
        [
            "/do-plan auth",
            "/do-task",
            "/do-commit",
            "/do-progress feature",
        ],
    )
    def test_command_prompts(self, analyze_func, prompt):
        """Prompts starting with '/' should return 'command'."""
        assert analyze_func(prompt) == "command"

    def test_unknown_prompt(self, analyze_func):
        """Short prompts without keywords should return 'unknown'."""
        assert analyze_func("hello") == "unknown"


class TestGatekeeperIntegration:
    """Integration tests for gatekeeper hook."""

    @pytest.fixture
    def hook_path(self, hooks_dir):
        return hooks_dir / "gatekeeper.py"

    def test_exit_code_always_zero(self, hook_path):
        """Gatekeeper should always exit 0 (never blocks)."""
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="any prompt here",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_complex_prompt_shows_warning(self, hook_path):
        """Complex prompts should produce warning on stderr."""
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="implement a new authentication system",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "[Gatekeeper]" in result.stderr
        assert "/do-plan" in result.stderr

    def test_simple_prompt_no_warning(self, hook_path):
        """Simple prompts should not produce warning."""
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="fix typo",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_command_prompt_no_warning(self, hook_path):
        """Command prompts should not produce warning."""
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="/do-plan feature",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stderr == ""

    def test_empty_input(self, hook_path):
        """Empty input should not crash."""
        result = subprocess.run(
            [sys.executable, str(hook_path)],
            input="",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
