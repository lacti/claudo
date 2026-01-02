#!/usr/bin/env bats

# Test suite for deploy.sh

setup() {
    # Load bats helpers if available
    if [[ -f "$BATS_TEST_DIRNAME/test_helper/bats-support/load.bash" ]]; then
        load 'test_helper/bats-support/load'
        load 'test_helper/bats-assert/load'
    fi

    # Save original HOME
    export ORIGINAL_HOME="$HOME"

    # Create isolated test environment
    export HOME="$BATS_TEST_TMPDIR/home"
    mkdir -p "$HOME/.claude"

    # Get script and project paths
    export SCRIPT_PATH="$BATS_TEST_DIRNAME/../../scripts/deploy.sh"
    export PROJECT_DIR="$BATS_TEST_DIRNAME/../.."

    # Initialize git repo in target directory
    cd "$HOME/.claude"
    git init
    git config user.email "test@test.com"
    git config user.name "Test User"
    echo "initial" > .gitkeep
    git add .
    git commit -m "Initial commit"

    # Create initial settings.json
    cat > "$HOME/.claude/settings.json" << 'EOF'
{
    "existing_key": "preserved",
    "commands": [],
    "hooks": {}
}
EOF
    git add settings.json
    git commit -m "Add settings"
}

teardown() {
    export HOME="$ORIGINAL_HOME"
}

@test "deploy.sh fails if ~/.claude is not a git repository" {
    rm -rf "$HOME/.claude/.git"

    run "$SCRIPT_PATH"

    [ "$status" -eq 1 ]
    [[ "$output" == *"not a git repository"* ]]
}

@test "deploy.sh copies hooks directory" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]
    [ -d "$HOME/.claude/hooks" ]
    [ -f "$HOME/.claude/hooks/gatekeeper.py" ]
    [ -f "$HOME/.claude/hooks/auto_logger.py" ]
    [ -f "$HOME/.claude/hooks/quality_gate.py" ]
}

@test "deploy.sh copies commands directory" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]
    [ -d "$HOME/.claude/commands" ]
    [ -f "$HOME/.claude/commands/do-plan.md" ]
    [ -f "$HOME/.claude/commands/do-task.md" ]
}

@test "deploy.sh preserves existing settings" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]

    # Check that existing_key is preserved
    run grep -c "existing_key" "$HOME/.claude/settings.json"
    [ "$output" = "1" ]
}

@test "deploy.sh transforms paths in settings.json" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]

    # Check that $CLAUDE_PROJECT_DIR is NOT present
    run grep -c 'CLAUDE_PROJECT_DIR' "$HOME/.claude/settings.json"
    [ "$output" = "0" ]
}

@test "deploy.sh creates git commit" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]

    cd "$HOME/.claude"
    run git log --oneline -1

    [[ "$output" == *"Deploy from"* ]]
}

@test "deploy.sh shows no changes message when rerun" {
    # First deployment
    "$SCRIPT_PATH"

    # Second deployment (no changes)
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]
    [[ "$output" == *"No changes to deploy"* ]]
}

@test "deploy.sh requires jq to be installed" {
    # This test verifies the script uses jq
    # jq should be installed for the test to pass
    command -v jq >/dev/null 2>&1 || skip "jq not installed"

    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]
}
