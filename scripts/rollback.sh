#!/bin/bash
set -e

TARGET_DIR="$HOME/.claude"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if ~/.claude is a git repository
if [ ! -d "$TARGET_DIR/.git" ]; then
    echo -e "${RED}Error: $TARGET_DIR is not a git repository${NC}"
    exit 1
fi

cd "$TARGET_DIR"

# If no argument, show deployment history
if [ -z "$1" ]; then
    echo -e "${GREEN}=== Deployment History ===${NC}"
    echo ""
    git log --oneline -20 --format="%C(yellow)%h%C(reset) %C(cyan)%cd%C(reset) %s" --date=format:"%Y-%m-%d %H:%M"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  rollback.sh <commit>  # Rollback to specific version"
    echo "  rollback.sh HEAD~1    # Rollback to previous version"
    echo ""
    echo -e "${YELLOW}Current version:${NC} $(git rev-parse --short HEAD)"
    exit 0
fi

TARGET_COMMIT="$1"

# Check if target commit exists
if ! git rev-parse "$TARGET_COMMIT" >/dev/null 2>&1; then
    echo -e "${RED}Error: Commit '$TARGET_COMMIT' not found${NC}"
    exit 1
fi

# Save current state
CURRENT_COMMIT=$(git rev-parse --short HEAD)
TARGET_SHORT=$(git rev-parse --short "$TARGET_COMMIT")

echo -e "${GREEN}=== Executing Rollback ===${NC}"
echo -e "Current: ${RED}$CURRENT_COMMIT${NC}"
echo -e "Target:  ${GREEN}$TARGET_SHORT${NC}"
echo ""

# Show target commit info
echo -e "${YELLOW}Target commit info:${NC}"
git log -1 --format="  %h %cd %s" --date=format:"%Y-%m-%d %H:%M" "$TARGET_COMMIT"
echo ""

# Confirmation
read -p "Proceed with rollback? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback cancelled."
    exit 0
fi

# Rollback only hooks and commands (leave other files untouched)
echo ""
echo -e "${GREEN}Restoring hooks and commands...${NC}"

# Restore hooks and commands from target commit
git checkout "$TARGET_COMMIT" -- hooks/ commands/ 2>/dev/null || {
    echo -e "${YELLOW}Warning: Some files may not exist in target commit${NC}"
    git checkout "$TARGET_COMMIT" -- hooks/ 2>/dev/null || true
    git checkout "$TARGET_COMMIT" -- commands/ 2>/dev/null || true
}

# Create rollback commit
git add hooks/ commands/
ROLLBACK_MSG="Rollback to $TARGET_SHORT (from $CURRENT_COMMIT)"
git commit -m "$ROLLBACK_MSG" --allow-empty

FINAL_COMMIT=$(git rev-parse --short HEAD)
echo ""
echo -e "${GREEN}=== Rollback Complete ===${NC}"
echo -e "New commit: ${GREEN}$FINAL_COMMIT${NC}"
echo ""
echo -e "${YELLOW}Note:${NC} To undo this rollback, run:"
echo "  ./scripts/rollback.sh $CURRENT_COMMIT"
