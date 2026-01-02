"""Tests for command markdown file syntax validation."""
import re
from pathlib import Path

import pytest
import yaml


def get_command_files():
    """Get all command markdown files."""
    commands_dir = Path(__file__).parents[2] / ".claude" / "commands"
    return list(commands_dir.glob("*.md"))


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    pattern = r"^---\s*\n(.*?)\n---"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            # Try parsing with quotes around problematic values
            yaml_text = match.group(1)
            # Handle argument-hint with spaces that looks like YAML arrays
            yaml_text = re.sub(
                r'^(argument-hint:\s*)(.+)$',
                lambda m: f'{m.group(1)}"{m.group(2)}"' if '[' in m.group(2) and not m.group(2).strip().startswith('"') else m.group(0),
                yaml_text,
                flags=re.MULTILINE
            )
            try:
                return yaml.safe_load(yaml_text)
            except yaml.YAMLError:
                return {}
    return {}


class TestCommandSyntax:
    """Validate all command markdown files."""

    @pytest.fixture(params=get_command_files(), ids=lambda p: p.name)
    def command_file(self, request):
        return request.param

    def test_file_exists_and_readable(self, command_file):
        """Command file should exist and be readable."""
        assert command_file.exists()
        content = command_file.read_text()
        assert len(content) > 0

    def test_has_yaml_frontmatter(self, command_file):
        """Command file should start with YAML frontmatter."""
        content = command_file.read_text()
        assert content.startswith("---"), f"{command_file.name}: Missing YAML frontmatter"

    def test_frontmatter_is_valid_yaml(self, command_file):
        """YAML frontmatter should be valid."""
        content = command_file.read_text()
        frontmatter = extract_frontmatter(content)
        assert frontmatter is not None, f"{command_file.name}: Invalid YAML frontmatter"
        assert isinstance(frontmatter, dict)

    def test_has_description(self, command_file):
        """Command should have a description field."""
        content = command_file.read_text()
        frontmatter = extract_frontmatter(content)
        assert "description" in frontmatter, f"{command_file.name}: Missing description"
        assert len(frontmatter["description"]) > 0

    def test_has_allowed_tools(self, command_file):
        """Command should specify allowed-tools."""
        content = command_file.read_text()
        frontmatter = extract_frontmatter(content)
        assert (
            "allowed-tools" in frontmatter
        ), f"{command_file.name}: Missing allowed-tools"
        assert isinstance(frontmatter["allowed-tools"], list)
        assert len(frontmatter["allowed-tools"]) > 0

    def test_has_model(self, command_file):
        """Command should specify a model."""
        content = command_file.read_text()
        frontmatter = extract_frontmatter(content)
        assert "model" in frontmatter, f"{command_file.name}: Missing model"

    def test_has_markdown_heading(self, command_file):
        """Command body should have at least one markdown heading."""
        content = command_file.read_text()
        # Remove frontmatter
        body = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL)
        assert re.search(
            r"^#\s+", body, re.MULTILINE
        ), f"{command_file.name}: Missing markdown heading"

    def test_allowed_tools_are_valid(self, command_file):
        """Allowed tools should be from the known set."""
        known_tools = {
            "Bash",
            "Write",
            "Read",
            "Glob",
            "Grep",
            "Edit",
            "Ls",
            "Task",
            "TodoWrite",
            "AskUserQuestion",
            "WebFetch",
            "WebSearch",
        }
        content = command_file.read_text()
        frontmatter = extract_frontmatter(content)
        tools = frontmatter.get("allowed-tools", [])
        for tool in tools:
            assert (
                tool in known_tools
            ), f"{command_file.name}: Unknown tool '{tool}'"


class TestAllCommandsPresent:
    """Ensure expected commands exist."""

    def test_expected_commands_exist(self, commands_dir):
        """All expected command files should exist."""
        expected = [
            "do-plan.md",
            "do-task.md",
            "do-commit.md",
            "do-progress.md",
            "do-deploy.md",
        ]
        for cmd in expected:
            assert (commands_dir / cmd).exists(), f"Missing command: {cmd}"

    def test_command_naming_convention(self, commands_dir):
        """Command files should follow naming convention."""
        for cmd_file in commands_dir.glob("*.md"):
            assert cmd_file.name.startswith(
                "do-"
            ), f"{cmd_file.name}: Should start with 'do-'"
