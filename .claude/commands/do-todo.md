---
description: Convert reviewed plan from plan mode to TODO task files
allowed-tools: ["Bash", "Write", "Read", "Glob"]
model: claude-opus-4-5-20251101
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

## Step 4: Create Base Files
Write the following files to `TODO/$1/`:

### 4.1 Write PLAN.md
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

### 4.2 Write checklist.md
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

### 4.3 Write progress.md
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

## Step 5: Create Task Files
**IMPORTANT: Each task MUST be created as a separate .md file.**

For EACH step/phase identified in Step 2, create a separate file:

### 5.1 Write 01.md
```markdown
# Task 01: {title}
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

### 5.2 Write 02.md, 03.md, ... (repeat for each task)
Use the same template. One file per task.

## Step 6: Verify All Files Created
```bash
ls TODO/$1/
```
Expected output must include: PLAN.md, checklist.md, progress.md, 01.md, 02.md, ...

## Step 7: Done
```
Done. TODO/$1/ created from {PLAN_FILE} with PLAN.md, checklist.md, progress.md, and task files (01.md, 02.md, ...).
Next: /do-task $1 | /do-progress $1
```
