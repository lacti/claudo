---
description: Convert reviewed plan from plan mode to TODO task files
allowed-tools: ["Bash", "Write", "Read", "Glob"]
model: claude-3-5-sonnet-20241022
argument-hint: <task-name>
---

# Plan to TODO Conversion

## Input
`$1` = task_name (use hyphens: `auth-system`)

## Step 1: Find Plan File
```bash
PLAN_FILE=$(ls -t ~/.claude/plans/*.md 2>/dev/null | head -1)
```
If not found:
```
Plan not found. Complete planning in plan mode first, then run /do-todo <name>
```

## Step 2: Analyze Plan
Extract: Title, Overview, Steps/Phases, Files to modify

## Step 3: Create Directory
```bash
mkdir -p TODO/$1
```

## Step 4: Generate Files

### PLAN.md
```markdown
# $1 Plan
## Overview
{from plan}
## Goals
- [ ] Goal 1
## Phases
### Phase 1: {name}
Task: 01.md, Summary
## Affected Files
- `path/file` - reason
## Source
{PLAN_FILE path}, {modified time}
```

### checklist.md
```markdown
# $1 Checklist
## Implementation
- [ ] {from each step}
## Code Quality
- [ ] Lint passed
- [ ] Tests passed
- [ ] Type check passed
## Verification
- [ ] Manual test
- [ ] Edge cases
```

### progress.md
```markdown
# $1 Progress
## Status: 🟡 Planning Done
### Timeline
- [{now}] Converted from {PLAN_FILE}
### Tasks
| Task | Status | Done At |
|------|--------|---------|
| 01.md | ⏳ | - |
### Rate
0/{total} (0%)
```

### Task files (01.md, 02.md...)
```markdown
# Task NN: {title}
## Goal
{from step}
## Steps
1. {from step content}
## File Changes
- `path/file` - {what}
## Done When
- [ ] {criterion}
## Notes
Source: Step N from {PLAN_FILE}
```

## Step 5: Done
```
Done. TODO/$1/ created from {PLAN_FILE}.
Next: /do-task $1 | /do-progress $1
```
