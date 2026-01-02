# Claudo

**Claudo** = Claude + do. A project for developing and managing Claude Code Hooks and Commands.

## Components

### Hooks

| Hook              | Trigger          | Description                             |
| ----------------- | ---------------- | --------------------------------------- |
| `gatekeeper.py`   | UserPromptSubmit | Recommends `/do-plan` for complex tasks |
| `quality_gate.py` | Stop             | Quality verification on task completion |

### Commands

| Command        | Description                                                       |
| -------------- | ----------------------------------------------------------------- |
| `/do-plan`     | Create implementation plan and task files (interactive or from plan mode) |
| `/do-task`     | Identify and execute next task automatically                      |
| `/do-commit`   | Analyze changes and create git commit                             |
| `/do-progress` | Display progress based on checklist.md                            |
| `/do-deploy`   | Read DEPLOY.md and run deployment process                         |

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/lacti/claudo.git
cd claudo

# 2. Install (first time only)
./scripts/deploy.sh

# 3. Add MCP server (optional)
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

## Documentation

- [INSTALL.md](./INSTALL.md) - Installation guide
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide
- [CLAUDE.md](./CLAUDE.md) - Development guide

## Directory Structure

```
claudo/
├── .claude/
│   ├── hooks/           # Hook scripts
│   ├── commands/        # Command definitions
│   └── settings.json    # Development settings
├── scripts/
│   ├── deploy.sh        # Deploy script
│   └── rollback.sh      # Rollback script
├── README.md
├── INSTALL.md
├── DEPLOYMENT.md
└── CLAUDE.md
```

## Workflow

```
[Development] Modify hooks, commands in .claude/
   ↓
[Testing] Run Claude Code in this project
   ↓
[Deploy] ./scripts/deploy.sh
   ↓
[Production] All projects use ~/.claude/
```

## License

MIT
