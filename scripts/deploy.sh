#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$HOME/.claude"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Claudo Deployment ===${NC}"
echo "Source: $PROJECT_DIR/.claude/"
echo "Target: $TARGET_DIR/"
echo ""

# Get git info from source project
cd "$PROJECT_DIR"
SOURCE_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
SOURCE_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
SOURCE_MSG=$(git log -1 --format="%s" 2>/dev/null || echo "unknown")

echo -e "${YELLOW}Source commit:${NC} $SOURCE_COMMIT ($SOURCE_BRANCH)"
echo -e "${YELLOW}Source message:${NC} $SOURCE_MSG"
echo ""

# Check if ~/.claude is a git repository
if [ ! -d "$TARGET_DIR/.git" ]; then
    echo -e "${RED}Error: $TARGET_DIR is not a git repository${NC}"
    echo "Initialize with: cd ~/.claude && git init"
    exit 1
fi

# Check status before deployment
cd "$TARGET_DIR"
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Warning: Uncommitted changes in $TARGET_DIR${NC}"
    git status --short
    echo ""
fi

# Copy files
echo -e "${GREEN}Copying files...${NC}"
cp -r "$PROJECT_DIR/.claude/hooks" "$TARGET_DIR/"
cp -r "$PROJECT_DIR/.claude/commands" "$TARGET_DIR/"

# Merge settings.json (preserve existing settings + add commands/hooks from project)
echo -e "${GREEN}Merging settings.json...${NC}"
SOURCE_SETTINGS="$PROJECT_DIR/.claude/settings.json"
TARGET_SETTINGS="$TARGET_DIR/settings.json"

if [ -f "$SOURCE_SETTINGS" ] && [ -f "$TARGET_SETTINGS" ]; then
    # Extract commands and hooks from project and merge with existing settings
    # Path transformation: $CLAUDE_PROJECT_DIR/.claude/ → ~/.claude/
    # jq: existing settings + project commands/hooks (project values take priority)
    MERGED=$(jq -s '
        .[0] as $target |
        .[1] as $source |

        # hooks path transformation function
        def transform_hooks:
            if . then
                walk(
                    if type == "string" then
                        gsub("\"\\$CLAUDE_PROJECT_DIR\"/.claude/"; "~/.claude/") |
                        gsub("\\$CLAUDE_PROJECT_DIR/.claude/"; "~/.claude/")
                    else .
                    end
                )
            else null
            end;

        # commands path transformation (file field)
        def transform_commands:
            if . then
                map(
                    if .file then
                        .file |= (
                            gsub("\"\\$CLAUDE_PROJECT_DIR\"/.claude/"; "~/.claude/") |
                            gsub("\\$CLAUDE_PROJECT_DIR/.claude/"; "~/.claude/")
                        )
                    else .
                    end
                )
            else null
            end;

        $target * {
            commands: (($source.commands | transform_commands) // $target.commands),
            hooks: (($source.hooks | transform_hooks) // $target.hooks)
        }
    ' "$TARGET_SETTINGS" "$SOURCE_SETTINGS")

    echo "$MERGED" > "$TARGET_SETTINGS"
    echo "  - commands, hooks merged (path conversion: \$CLAUDE_PROJECT_DIR → ~/.claude)"
elif [ -f "$SOURCE_SETTINGS" ] && [ ! -f "$TARGET_SETTINGS" ]; then
    # Copy if target doesn't have settings.json
    cp "$SOURCE_SETTINGS" "$TARGET_SETTINGS"
    echo "  - settings.json copied"
fi

# Check for changes
cd "$TARGET_DIR"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}No changes to deploy${NC}"
    exit 0
fi

# Git commit
echo ""
echo -e "${GREEN}Committing changes...${NC}"
git add hooks/ commands/ settings.json
DEPLOY_MSG="Deploy from $SOURCE_BRANCH@$SOURCE_COMMIT: $SOURCE_MSG"
git commit -m "$DEPLOY_MSG"

# Output results
DEPLOY_COMMIT=$(git rev-parse --short HEAD)
echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo -e "Deployed commit: ${GREEN}$DEPLOY_COMMIT${NC}"
echo ""
echo -e "${YELLOW}Rollback:${NC}"
echo "  ./scripts/rollback.sh          # View recent deployments"
echo "  ./scripts/rollback.sh <commit> # Rollback to specific version"
