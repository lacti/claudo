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
   - Read the file and parse JSON, extract `feature` field
   - Check if `TODO/{feature}/` directory exists
   - Show: "Existing session found (feature: {feature}, started: {started_at})"
   - Ask: "How do you want to proceed?"
     - `[C] Continue` - Add new tasks to existing plan (keeps progress)
     - `[N] New` - Start fresh (existing TODO/{feature} will be overwritten)
     - `[X] Cancel` - Exit without changes
   - **STOP and WAIT for user response.**
   - If user selects C: Go to **Step 0.1 (Continue Mode)**
   - If user selects N: proceed to Step 1
   - If user selects X: exit without changes

## Step 0.1: Continue Mode (Add Tasks to Existing Plan)
**Use this when Final Review identified additional work needed**

1. Load existing context:
   - Read `TODO/{feature}/PLAN.md`
   - Read `TODO/{feature}/requirements.md`
   - Read `TODO/{feature}/checklist.md`
   - Read `TODO/{feature}/progress.md`
2. List completed and pending tasks from progress.md
3. Ask user: "What additional implementation is needed?"
   **STOP and WAIT for user response.**
4. Analyze new requirements (apply Step 3 guidelines)
5. Identify Final Review task and determine insertion point:
   ```bash
   # Find current Final Review task (contains "Final Review" in title)
   grep -l "Final Review" TODO/{feature}/[0-9]*.md
   ```
   - Note the Final Review task number (e.g., 03.md)
   - New tasks will use that number onwards
   - Final Review will be renumbered to last
6. Renumber and create task files:
   - Rename existing Final Review task to new last number
   - Create new task files at the freed numbers
   - Example: If Final Review was 03.md and adding 2 tasks:
     - Rename 03.md → 05.md (Final Review)
     - Create 03.md (new task 1)
     - Create 04.md (new task 2)
7. Update PLAN.md: Add new phase/tasks
8. Update progress.md: Add new tasks to table
9. Update checklist.md: Add new verification items if needed
10. Report:
    ```
    Added {N} new task(s) to {feature}:
    - {XX}.md: {title}
    - {YY}.md: {title}

    Note: Final Review task remains as last task.
    Next: /do-task
    ```
11. **Exit (do not proceed to Step 1)**

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

## Step 3: Comprehensive Analysis

### 3.1 Requirement Breakdown
Break down requirements to prevent omissions:
- Core: Must-have functionality
- Support: Auxiliary features (validation, error handling, etc.)
- Integration: Connection with existing code
- Quality: Tests, documentation

### 3.2 Task Sizing Guidelines
Each Task must meet these criteria:
- 1 Task = 1 clear goal
- Expected file changes: 1-5 files
- Expected line changes: 50-300 lines
- Too large → split, Too small → merge

### 3.3 Completeness Checklist
Before splitting tasks, verify:
- [ ] Error handling included?
- [ ] Edge cases covered?
- [ ] Tests included?
- [ ] Existing code modifications included?
- [ ] Config/env changes included?
- [ ] Type definitions added/modified?

### 3.4 Derive File Changes
List all files that need modification

### 3.5 Review Integration
Review integration approach with existing code

### 3.6 Identify Risks
Identify potential risks

### 3.7 Split into Tasks
Based on above analysis, split into tasks (01, 02, 03...)

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
| ... | ... | ... |
| {XX}.md | ⏳ | - | ← Final Review
### Rate
0/{total} (0%)
```
Note: The last task is always "Final Review" (created in Step 6.3)

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

### 6.3 Write Final Review Task (MANDATORY)
**Always create this as the last task file (e.g., if last implementation task is 03.md, create 04.md)**

```markdown
# Task {XX}: Final Review

## Goal
Final verification based on checklist.md after all implementation is complete

## Steps
1. Load `checklist.md` and verify all items
2. Code quality verification:
   ```bash
   npm run lint && npm run test && npm run typecheck
   ```
3. Functional verification: Review implementation against requirements.md
4. Code review:
   - Identify missing implementations
   - Identify duplicate implementations
   - Identify unnecessary implementations
5. Fix discovered issues (minor fixes only)
6. Update checklist.md with results

## Done When
- [ ] All checklist items are `[x]`
- [ ] lint/test/typecheck passed
- [ ] Missing/duplicate/unnecessary implementation review completed

## Notes
If additional implementation is required after completing this task:
→ **DO NOT delete `.do-session`** and report:
```
Additional implementation required.

Issues found:
- {issue 1}
- {issue 2}

Session: Active (not completed)
Next: /do-plan {FEATURE_NAME}
```
```

## Step 7: Verify All Files Created
```bash
ls TODO/{FEATURE_NAME}/
```
Expected output must include: PLAN.md, requirements.md, checklist.md, progress.md, 01.md, 02.md, ..., {XX}.md (Final Review)

## Step 8: Done
```
Done. TODO/{FEATURE_NAME}/ created with:
- PLAN.md, requirements.md, checklist.md, progress.md
- Task files: 01.md ~ {XX}.md (last is Final Review)
{If from plan file: "Converted from {filename only, no path}"}
Next: /do-task | /do-progress
```
