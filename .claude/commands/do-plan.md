---
description: Create implementation plan and task files (interactive or from plan mode)
allowed-tools: ["Bash", "Write", "Read", "Glob", "Grep"]
model: claude-opus-4-5-20251101
argument-hint: <feature-name> [--from-plan]
---

# Feature Planning

## Input
- `$1` = feature_name (use hyphens: `auth-system`)
- `--from-plan`: Convert from latest plan mode file

## Step 1: Gather Requirements

### If --from-plan flag:
```bash
PLAN_FILE=$(ls -t ~/.claude/plans/*.md 2>/dev/null | head -1)
```
If not found: `Plan not found. Complete planning in plan mode first.`
Else: Read and extract title, overview, steps, files from PLAN_FILE.

### If no --from-plan:
If `$2` empty, ask:
```
Planning $1. Provide:
- Required functionality
- Main user scenarios
- Technical constraints
```
Else use `$ARGUMENTS` after `$1`.

## Step 2: Context
1. Check `@CLAUDE.md` for tech stack
2. `!git status`
3. Search related code

## Step 3: Analyze
- Derive file changes
- Review integration approach
- Identify risks
- Split into tasks (01, 02, 03...)

## Step 4: Create Directory
```bash
mkdir -p TODO/$1
```

## Step 5: Create Base Files
Write the following files to `TODO/$1/`:

### 5.1 Write PLAN.md
```markdown
# $1 Plan
## Overview
{summary}
## Goals
- [ ] Goal 1
## Phases
### Phase 1: {name}
Task: 01.md, Summary
## Affected Files
- `path/file.ts` - reason
## Technical Notes
{dependencies, risks}
## Source
{If --from-plan: PLAN_FILE path and modified time}
```

### 5.2 Write requirements.md
```markdown
# $1 Requirements
## Original Request
{user input}
## Analyzed
1. ...
## Acceptance Criteria
- [ ] Criterion 1
```

### 5.3 Write checklist.md
```markdown
# $1 Checklist
## Functional
- [ ] {from requirements}
## Code Quality
- [ ] Lint passed
- [ ] Tests passed
- [ ] Type check passed
## Verification
- [ ] Manual test
- [ ] Edge cases
```

### 5.4 Write progress.md
```markdown
# $1 Progress
## Status: 🟡 Planning Done
### Timeline
- [{now}] Planning done
### Tasks
| Task | Status | Done At |
|------|--------|---------|
| 01.md | ⏳ | - |
### Rate
0/{total} (0%)
```

## Step 6: Create Task Files
**IMPORTANT: Each task MUST be created as a separate .md file.**

For EACH task identified in Step 3, create a separate file:

### 6.1 Write 01.md
```markdown
# Task 01: {title}
## Goal
{specific goal}
## Steps
1. {step}
## File Changes
- `path/file.ts` - {what}
## Done When
- [ ] {criterion}
## Notes
{dependencies}
```

### 6.2 Write 02.md, 03.md, ... (repeat for each task)
Use the same template. One file per task.

Rules: Each task independent, clear dependencies stated.

## Step 7: Verify All Files Created
```bash
ls TODO/$1/
```
Expected output must include: PLAN.md, requirements.md, checklist.md, progress.md, 01.md, 02.md, ...

## Step 8: Done
```
Done. TODO/$1/ created with PLAN.md, requirements.md, checklist.md, progress.md, and task files.
{If --from-plan: "Converted from {PLAN_FILE}"}
Next: /do-task $1 | /do-progress $1
```
