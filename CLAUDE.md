# Claudo Development Guide

## Development Environment Setup

Running Claude Code in this project applies settings from `.claude/settings.json`.
Hooks under development use the `$CLAUDE_PROJECT_DIR/.claude/hooks/` path.

## Core Rules

### 1. Path Rules

**Development Environment (this project)**

```
$CLAUDE_PROJECT_DIR/.claude/hooks/xxx.py
$CLAUDE_PROJECT_DIR/.claude/commands/xxx.md
```

**Production Environment (~/.claude/)**

```
~/.claude/hooks/xxx.py
~/.claude/commands/xxx.md
```

- Development: Use `$CLAUDE_PROJECT_DIR`
- Deployment: `deploy.sh` auto-converts to `~/.claude`

### 2. settings.json Modification Notes

When modifying `.claude/settings.json`:

- Only `commands` and `hooks` keys are deployed
- Other keys (e.g., `model`, `mcpServers`) are not deployed
- Existing settings in `~/.claude/settings.json` are preserved during deployment

### 3. Hook Development Rules

```python
#!/usr/bin/env python3
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read()

    # Processing logic

    # stdout: Message to display to user
    # stderr: Log/warning messages
    # exit(0): Success, exit(1): Block
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Hook Input by Type**

| Hook             | stdin Input                  |
| ---------------- | ---------------------------- |
| UserPromptSubmit | User prompt                  |
| PostToolUse      | Tool execution result (JSON) |
| Stop             | Session info                 |

### 4. Command Development Rules

Create Markdown files under `.claude/commands/`:

```markdown
# Command: do-example

## Purpose

Describe the purpose of this command.

## Preconditions

- Condition 1
- Condition 2

## Prompt

Write instructions to be passed to Claude.
```

### 5. Testing

**IMPORTANT: All changes MUST pass tests before deployment.**

1. Run `make test` to execute all tests
2. All tests must pass before any code changes are merged or deployed
3. Run Claude Code in this project directory for manual testing
4. Hooks/commands under development are applied
5. Deploy only after all tests pass

```bash
# Run tests (REQUIRED before deployment)
make test

# Deploy after all tests pass
./scripts/deploy.sh
```

## File Structure Rules

```
.claude/
├── hooks/
│   └── *.py          # Python scripts, require execute permission
├── commands/
│   └── *.md          # Markdown format
└── settings.json     # Development settings
```

## Pre-Deployment Checklist

- [ ] **All tests pass (`make test`)** ← REQUIRED
- [ ] Hook scripts have execute permission (`chmod +x`)
- [ ] Paths use `$CLAUDE_PROJECT_DIR`
- [ ] stdin/stdout/stderr used correctly
- [ ] Exit codes returned correctly
- [ ] Tested in this project
