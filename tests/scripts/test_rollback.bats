#!/usr/bin/env bats

# Test suite for rollback.sh

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

    # Get script path
    export SCRIPT_PATH="$BATS_TEST_DIRNAME/../../scripts/rollback.sh"

    # Initialize git repo with history
    cd "$HOME/.claude"
    git init
    git config user.email "test@test.com"
    git config user.name "Test User"

    # Create initial version
    mkdir -p hooks commands
    echo "version1" > hooks/test.py
    echo "version1" > commands/test.md
    git add .
    git commit -m "Version 1"
    export V1_COMMIT=$(git rev-parse HEAD)

    # Create second version
    echo "version2" > hooks/test.py
    echo "version2" > commands/test.md
    git add .
    git commit -m "Version 2"
    export V2_COMMIT=$(git rev-parse HEAD)

    # Create third version (current)
    echo "version3" > hooks/test.py
    echo "version3" > commands/test.md
    git add .
    git commit -m "Version 3"
    export V3_COMMIT=$(git rev-parse HEAD)
}

teardown() {
    export HOME="$ORIGINAL_HOME"
}

@test "rollback.sh fails if ~/.claude is not a git repository" {
    rm -rf "$HOME/.claude/.git"

    run "$SCRIPT_PATH"

    [ "$status" -eq 1 ]
    [[ "$output" == *"not a git repository"* ]]
}

@test "rollback.sh shows history without arguments" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]
    [[ "$output" == *"Deployment History"* ]]
    [[ "$output" == *"Version 1"* ]]
    [[ "$output" == *"Version 2"* ]]
    [[ "$output" == *"Version 3"* ]]
}

@test "rollback.sh shows usage info" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]
    [[ "$output" == *"Usage"* ]]
    [[ "$output" == *"rollback.sh"* ]]
}

@test "rollback.sh shows current version" {
    run "$SCRIPT_PATH"

    [ "$status" -eq 0 ]
    [[ "$output" == *"Current version"* ]]
}

@test "rollback.sh fails for non-existent commit" {
    run "$SCRIPT_PATH" "nonexistent123"

    [ "$status" -eq 1 ]
    [[ "$output" == *"not found"* ]]
}

@test "rollback.sh shows target commit info" {
    # Run with 'n' to cancel
    run bash -c "echo 'n' | '$SCRIPT_PATH' '$V1_COMMIT'"

    [ "$status" -eq 0 ]
    [[ "$output" == *"Target commit info"* ]]
    [[ "$output" == *"Version 1"* ]]
}

@test "rollback.sh cancels on 'n' input" {
    run bash -c "echo 'n' | '$SCRIPT_PATH' '$V1_COMMIT'"

    [ "$status" -eq 0 ]
    [[ "$output" == *"Rollback cancelled"* ]]

    # Verify files unchanged
    [ "$(cat "$HOME/.claude/hooks/test.py")" = "version3" ]
}

@test "rollback.sh restores files on 'y' input" {
    run bash -c "echo 'y' | '$SCRIPT_PATH' '$V1_COMMIT'"

    [ "$status" -eq 0 ]
    [[ "$output" == *"Rollback Complete"* ]]

    # Verify files restored to v1
    [ "$(cat "$HOME/.claude/hooks/test.py")" = "version1" ]
    [ "$(cat "$HOME/.claude/commands/test.md")" = "version1" ]
}

@test "rollback.sh creates rollback commit" {
    bash -c "echo 'y' | '$SCRIPT_PATH' '$V1_COMMIT'"

    cd "$HOME/.claude"
    run git log --oneline -1

    [[ "$output" == *"Rollback to"* ]]
}

@test "rollback.sh shows undo instructions" {
    run bash -c "echo 'y' | '$SCRIPT_PATH' '$V1_COMMIT'"

    [ "$status" -eq 0 ]
    [[ "$output" == *"To undo this rollback"* ]]
}

@test "rollback.sh supports HEAD~N syntax" {
    run bash -c "echo 'y' | '$SCRIPT_PATH' 'HEAD~2'"

    [ "$status" -eq 0 ]
    [[ "$output" == *"Rollback Complete"* ]]

    # Should be at version 1 (2 commits back from v3)
    [ "$(cat "$HOME/.claude/hooks/test.py")" = "version1" ]
}
