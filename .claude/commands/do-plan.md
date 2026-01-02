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
- Feature name is auto-generated from request or plan content (use hyphens: `auth-system`)

## Step 0: Session Check

1. Check if `.claude/.do-session` exists
2. If exists:
   - Read the file and parse JSON
   - Show: "Existing session found (feature: {feature}, started: {started_at})"
   - Ask: "Start a new session? The existing session will be cancelled. (yes/no)"
   - **STOP and WAIT for user response.**
   - If user says no: exit without changes
   - If user says yes: proceed to Step 1

## Step 1: Gather Requirements

### If $ARGUMENTS has content (10+ characters):
Use it as the requirement directly.
Generate `FEATURE_NAME` from the request content (kebab-case, 2-4 words).
Proceed to Step 2.

### If $ARGUMENTS is empty or too brief:
1. Check for recent plan files:
```bash
ls -t ~/.claude/plans/*.md 2>/dev/null | head -4
```

2. **If plan files found:**
   Show a numbered list with preview (first 3 lines of each file):
   ```
   Recent plans found:
   1. curious-happy-penguin.md (2h ago)
      # User Authentication System
      ## Overview
      Implement OAuth2...
   2. silly-jumping-koala.md (1d ago)
      # API Rate Limiting
      ...
   [N] Enter new requirements
   ```
   **STOP and WAIT for user selection.**
   - If user selects 1-4: Read that plan file, extract title/overview/steps/files, generate `FEATURE_NAME` from plan title
   - If user selects N: Ask for requirements (see below)

3. **If no plan files found OR user selected N:**
   Ask the user:
   ```
   Please describe:
   - What functionality do you need?
   - Main use cases/scenarios?
   - Any technical constraints?
   ```
   **STOP and WAIT for user response.**
   Generate `FEATURE_NAME` from user's response (kebab-case, 2-4 words).

Only after gathering requirements, proceed to Step 2.

## Step 2: Context
1. Check `@CLAUDE.md` for tech stack
2. `!git status`
3. Search related code

## Step 3: Analyze
- Derive file changes
- Review integration approach
- Identify risks
- Split into tasks (01, 02, 03...)

## Step 4: Create Directory and Session
```bash
mkdir -p TODO/{FEATURE_NAME}
mkdir -p .claude
```

Create `.claude/.do-session`:
```json
{"feature": "{FEATURE_NAME}", "started_at": "{ISO8601 timestamp}", "phase": "planning"}
```
Note: `phase` is `planning` initially. It changes to `executing` when `/do-task` runs.

## Step 5: Create Base Files
Write the following files to `TODO/{FEATURE_NAME}/`:

### 5.1 Write PLAN.md
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
{dependencies, risks}
## Source
{If from plan file: Only filename (e.g., `plan-name.md`) and modified time. NEVER include full path or home directory.}
```

### 5.2 Write requirements.md
```markdown
# {FEATURE_NAME} Requirements
## Original Request
{user input}
## Analyzed
1. ...
## Acceptance Criteria
- [ ] Criterion 1
```

### 5.3 Write checklist.md
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

### 5.4 Write progress.md
```markdown
# {FEATURE_NAME} Progress
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
ls TODO/{FEATURE_NAME}/
```
Expected output must include: PLAN.md, requirements.md, checklist.md, progress.md, 01.md, 02.md, ...

## Step 8: Done
```
Done. TODO/{FEATURE_NAME}/ created with PLAN.md, requirements.md, checklist.md, progress.md, and task files.
{If from plan file: "Converted from {filename only, no path}"}
Next: /do-task {FEATURE_NAME} | /do-progress {FEATURE_NAME}
```
