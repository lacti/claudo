# Deployment Guide

## Deployment Process

### 1. Run Deployment

```bash
./scripts/deploy.sh
```

**Actions performed:**

1. Copy `.claude/hooks/` → `~/.claude/hooks/`
2. Copy `.claude/commands/` → `~/.claude/commands/`
3. Merge `settings.json` (preserve existing + add commands/hooks)
4. Auto-convert paths (`$CLAUDE_PROJECT_DIR` → `~/.claude`)
5. Create Git commit

**Example output:**

```
=== Claudo Deployment ===
Source: /home/user/git/claudo/.claude/
Target: /home/user/.claude/

Source commit: abc1234 (main)
Source message: Add new hook

Copying files...
Merging settings.json...
  - Merged commands, hooks (path conversion: $CLAUDE_PROJECT_DIR → ~/.claude)

Committing changes...
[main def5678] Deploy from main@abc1234: Add new hook

=== Deployment Complete ===
Deployed commit: def5678
```

### 2. Verify Deployment

```bash
# Check deployed files
ls -la ~/.claude/hooks/
ls -la ~/.claude/commands/

# Check settings.json
cat ~/.claude/settings.json

# View deployment history
./scripts/rollback.sh
```

## Rollback

### View Deployment History

```bash
./scripts/rollback.sh
```

**Example output:**

```
=== Deployment History ===

def5678 2026-01-02 12:05 Deploy from main@abc1234: Add new hook
abc1234 2026-01-02 11:55 Deploy from main@xyz9999: Initial
feea5a9 2026-01-02 11:53 Initial commit

Usage:
  rollback.sh <commit>  # Rollback to specific version
  rollback.sh HEAD~1    # Rollback to previous version

Current version: def5678
```

### Execute Rollback

```bash
# Rollback to specific commit
./scripts/rollback.sh abc1234

# Rollback to previous version
./scripts/rollback.sh HEAD~1
```

**Rollback confirmation prompt:**

```
=== Rollback Execution ===
Current: def5678
Target:  abc1234

Target commit info:
  abc1234 2026-01-02 11:55 Deploy from main@xyz9999: Initial

Proceed with rollback? (y/N)
```

## Deployment Structure

### Path Conversion

| Development Environment                 | Production Environment |
| --------------------------------------- | ---------------------- |
| `$CLAUDE_PROJECT_DIR/.claude/hooks/`    | `~/.claude/hooks/`     |
| `$CLAUDE_PROJECT_DIR/.claude/commands/` | `~/.claude/commands/`  |

### settings.json Merge

**Merged keys:**

- `commands` - Full replacement
- `hooks` - Full replacement (with path conversion)

**Preserved keys:**

- `model`
- `mcpServers`
- Other user settings

## Troubleshooting

### ~/.claude is not a git repository

```bash
cd ~/.claude
git init
git add .gitignore settings.json
git commit -m "Initial commit"
```

### jq not installed

```bash
# Ubuntu/Debian
sudo apt install jq

# macOS
brew install jq
```

### Hooks not working after deployment

1. Check permissions:

   ```bash
   chmod +x ~/.claude/hooks/*.py
   ```

2. Check paths:

   ```bash
   cat ~/.claude/settings.json | jq '.hooks'
   ```

3. Check Python path:
   ```bash
   which python3
   ```
