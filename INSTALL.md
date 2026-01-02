# Installation Guide

## Prerequisites

- Claude Code CLI installed
- Python 3.x
- jq (for JSON processing)
- Git

### Install jq

```bash
# Ubuntu/Debian
sudo apt install jq

# macOS
brew install jq

# Verify
jq --version
```

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/lacti/claudo.git ~/git/claudo
cd ~/git/claudo
```

### 2. Initialize ~/.claude Git Repository

```bash
# Navigate to ~/.claude directory
cd ~/.claude

# Initialize Git repository
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Exclude everything
*

# Include managed files
!.gitignore
!settings.json
!hooks/
!hooks/**
!commands/
!commands/**

# Exclude sensitive files
.credentials.json
EOF

# Initial commit
git add .gitignore settings.json
git commit -m "Initial commit: settings.json and .gitignore"
```

### 3. Run Deployment

```bash
cd ~/git/claudo
./scripts/deploy.sh
```

### 4. Verify Installation

```bash
# Check deployed files
ls ~/.claude/hooks/
ls ~/.claude/commands/

# Verify in Claude Code
claude
# Type /do- in prompt to see autocomplete
```

## Optional Configuration

### Add Chrome DevTools MCP Server

```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

### Model Configuration

Edit `~/.claude/settings.json` directly:

```json
{
  "model": "opus"
}
```

## Update

Pull latest changes and redeploy:

```bash
cd ~/git/claudo
git pull
./scripts/deploy.sh
```

## Uninstall

### Remove Hooks/Commands Only

```bash
rm -rf ~/.claude/hooks
rm -rf ~/.claude/commands
```

### Remove from settings.json

Delete `commands` and `hooks` keys from `~/.claude/settings.json`

## Troubleshooting

### "~/.claude is not a git repository" Error

```bash
cd ~/.claude
git init
git add .gitignore settings.json
git commit -m "Initial commit"
```

### Hook Permission Error

```bash
chmod +x ~/.claude/hooks/*.py
```

### Commands Not Visible in Claude Code

1. Restart Claude Code
2. Check settings.json:
   ```bash
   cat ~/.claude/settings.json | jq '.commands'
   ```

### Python Not Found

Verify Python 3 installation:

```bash
which python3
python3 --version
```
