---
description: Identify and execute next task automatically, review checklist on completion
allowed-tools: ["Bash", "Write", "Read", "Edit", "Ls"]
model: claude-3-5-sonnet-20241022
argument-hint: <feature-name>
---

# Auto-Resume Task Execution Protocol

**Target**: Automatically identify and execute remaining tasks in `TODO/$1` directory.

## 1. Context Loading (State Check)

Load the following context for task execution:

- **Project Rules**: `@CLAUDE.md` (coding conventions)
- **Feature Plan**: `@TODO/$1/PLAN.md` (overall plan)
- **Progress Log**: `@TODO/$1/progress.md` (current progress)

## 2. Next Task Identification (Reasoning)

**Determine the next task yourself:**

1. Run `ls TODO/$1` to check files in the directory
2. Analyze `progress.md` to identify completed tasks (`Completed` or `✅`)
3. Find the **next task file** in numerical order
   - Example: If `01.md` is completed, read and execute `02.md`

## 3. Task Execution (Implementation)

**If task files remain:**

1. Read the task file (e.g., `02.md`) using the `Read` tool
2. Write or modify code according to task instructions
3. Run tests/lint defined in `CLAUDE.md` after code changes
4. Record results in `progress.md`:
   ```markdown
   - [{current date/time}] 02.md Completed: {brief implementation summary}
   ```
5. Update task status table in progress.md:
   ```markdown
   | 02.md | ✅ Done | {current time} |
   ```

## 4. All Tasks Completed Check

**When all task files are completed:**

Perform **checklist review** in the following order:

### 4.1 Load Checklist

```
@TODO/$1/checklist.md
```

### 4.2 Verify Each Item

Check and verify each checklist item:

**Code Quality Items:**

```bash
# Lint check
npm run lint

# Run tests
npm run test

# Type check (if applicable)
npm run typecheck
```

**Functional Requirement Items:**

- Review implemented code to verify requirement fulfillment
- Fix any unmet items

### 4.3 Update Checklist

Update verified items with check marks:

```markdown
- [x] Lint passed (npm run lint)
- [x] Tests passed (npm run test)
```

### 4.4 Handle Incomplete Items

If incomplete items exist:

1. Perform work to resolve the item
2. Verify again
3. Repeat until all items are complete

### 4.5 Review Completion Report

When all checklist items are complete:

```
🎉 All tasks and checklist review completed!

📊 Final Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task files: {N} completed
✅ Checklist: All {M} items passed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next steps:
  /do-commit $1   - Commit changes
  /do-deploy      - Run deployment
```

## 5. Progress Update

Update progress.md status:

**Work in progress:**

```markdown
## Current Status: 🔵 In Progress (N/M completed)
```

**All tasks completed + checklist passed:**

```markdown
## Current Status: ✅ Implementation Complete

### Completion Rate

- Checklist: {M}/{M} (100%)
```

## 6. Report (When work is in progress)

```
✅ Task completed: {task_name}

Work performed:
  - {Change 1}
  - {Change 2}

Remaining tasks: {remaining_count}
  - {next_task_name}
  - ...

Next steps:
  /do-task $1       - Execute next task
  /do-progress $1   - Check progress
```
