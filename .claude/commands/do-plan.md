---
description: Create implementation plan and task files (interactive)
allowed-tools: ["Bash", "Write", "Read", "Glob", "Grep"]
model: claude-opus-4-5-20251101
argument-hint: <feature-name>
---

# Feature Planning (Interactive)

## Input
`$1` = feature_name (use hyphens: `auth-system`)

## Step 1: Gather Requirements
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

## Step 5: Generate Files

### PLAN.md
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
```

### requirements.md
```markdown
# $1 Requirements
## Original Request
{user input}
## Analyzed
1. ...
## Acceptance Criteria
- [ ] Criterion 1
```

### checklist.md
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

### progress.md
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

### Task files (01.md, 02.md...)
```markdown
# Task NN: {title}
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

Rules: Each task independent, clear dependencies stated.

## Step 6: Done
```
Done. TODO/$1/ created with PLAN.md, requirements.md, checklist.md, progress.md, task files.
Next: /do-task $1 | /do-progress $1
```
