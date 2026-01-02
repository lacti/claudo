---
description: Create implementation plan and task files (interactive or from plan mode)
allowed-tools: ["Bash", "Write", "Read", "Glob", "Grep"]
model: claude-opus-4-5-20251101
argument-hint: [<request>]
---

# Feature Planning

## Input
- `$ARGUMENTS` = request description (optional)
- If empty: Shows recent plan files from `~/.claude/plans/` for selection
- If provided: Uses the text as requirements
- Feature name is auto-generated from request or plan content (use hyphens, e.g., `auth-system`)

## Step 0: Session Check
1. Check `.claude/.do-session`
2. If exists:
   - Read file, parse JSON, extract `feature`
   - Check `TODO/{feature}/` exists
   - Show: "Existing session found (feature: {feature}, started: {started_at})"
   - Ask: "Proceed?"
     - `[C] Continue` - Add new tasks to existing plan (keeps progress)
     - `[N] New` - Start fresh (existing TODO/{feature} will be overwritten)
     - `[X] Cancel` - Exit without changes
   - **STOP and WAIT for response.**
   - C: Go to **Step 0.1**
   - N: Go to Step 1
   - X: Exit

## Step 0.1: Continue Mode
**Use when Final Review identified additional work**
1. Load context: `PLAN.md`, `requirements.md`, `checklist.md`, `progress.md` from `TODO/{feature}/`
2. List completed/pending tasks
3. Ask: "What additional implementation is needed?"
   **STOP and WAIT for response.**
4. Analyze new requirements (Step 3 guidelines)
5. Identify Final Review task (grep "Final Review"):
   - Note number (e.g., 03.md)
   - New tasks start here
   - Final Review renumbered to last
6. Create tasks:
   - Rename existing Final Review to new last number
   - Create new tasks at freed numbers
7. Update `PLAN.md` (new phase), `progress.md` (add tasks), `checklist.md` (new items)
8. Report: "Added {N} tasks. Final Review is last. Next: /do-task"
9. **Exit**

## Step 1: Gather Requirements

### If $ARGUMENTS has content (10+ chars):
Use directly. Generate `FEATURE_NAME` (kebab-case). proceed to Step 2.

### If $ARGUMENTS empty:
1. Check recent plans: `ls -t ~/.claude/plans/*.md 2>/dev/null | head -4`
2. **If found:**
   Show numbered list with preview (3 lines).
   Ask: "Select plan [1-4] or [N] ew requirements"
   **STOP and WAIT for selection.**
   - 1-4: Extract title/steps, generate `FEATURE_NAME`
   - N: Ask for requirements
3. **If none or N:**
   Ask: "Describe functionality, use cases, constraints"
   **STOP and WAIT for response.**
   Generate `FEATURE_NAME` (kebab-case).

## Step 2: Context
1. `@CLAUDE.md`
2. `!git status`
3. Search related code

## Step 3: Analysis & Breakdown
### 3.1 Breakdown
- Core, Support, Integration, Quality

### 3.2 Sizing
- 1 Task = 1 goal, 1-5 files, 50-300 lines

### 3.3 Completeness
- [ ] Errors, Edge cases, Tests, Existing code, Config, Types

### 3.4 Derive File Changes & Integration
List modified files and integration approach.

### 3.5 Split into Tasks (01, 02...)

## Step 4: Create Directory
```bash
mkdir -p TODO/{FEATURE_NAME} .claude
```
Write `.claude/.do-session`: `{"feature": "{FEATURE_NAME}", "started_at": "{ISO8601}", "phase": "planning"}`

## Step 5: Base Files (TODO/{FEATURE_NAME}/)

### 5.1 PLAN.md
```markdown
# {FEATURE_NAME} Plan
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
{notes}
## Source
{filename only if from plan}
```

### 5.2 requirements.md
```markdown
# {FEATURE_NAME} Requirements
## Original Request
{input}
## Analyzed
1. ...
## Acceptance Criteria
- [ ] Criterion 1
```

### 5.3 checklist.md
```markdown
# {FEATURE_NAME} Checklist
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

### 5.4 progress.md
```markdown
# {FEATURE_NAME} Progress
## Status: 🟡 Planning Done
### Timeline
- [{now}] Planning done
### Tasks
| Task | Status | Done At |
|------|--------|---------|
| 01.md | ⏳ | - |
| ... | ... | ... |
| {XX}.md | ⏳ | - | ← Final Review
### Rate
0/{total} (0%)
```
Last task is always "Final Review".

## Step 6: Task Files (01.md ... {XX}.md)
**One file per task.**

### 6.1 Task Template
```markdown
# Task {N}: {title}
## Goal
{goal}
## Steps
1. {step}
## File Changes
- `path/file.ts` - {what}
## Done When
- [ ] {criterion}
## Notes
{deps}
```

### 6.2 Final Review Task (MANDATORY, Last)
```markdown
# Task {XX}: Final Review
## Goal
Final verification.
## Steps
1. Verify all `checklist.md` items
2. Quality: `npm run lint && npm run test && npm run typecheck`
3. Func/Code Review: Check against requirements, find missing/dup code
4. Fix minor issues
5. Update `checklist.md`
## Done When
- [ ] Checklist objects [x]
- [ ] Quality checks pass
- [ ] Review complete
## Notes
If work remains → **DO NOT delete .do-session**. Report: "Additional implementation required. Issues: ... Next: /do-plan {FEATURE_NAME}"
```

## Step 7: Verify & Done
1. `ls TODO/{FEATURE_NAME}/` -> Expect PLAN, requirements, checklist, progress, 01...XX
2. Report:
```
Done. TODO/{FEATURE_NAME}/ created.
Tasks: 01.md ~ {XX}.md (Final Review)
Next: /do-task | /do-progress
```
