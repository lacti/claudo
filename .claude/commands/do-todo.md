---
description: Convert reviewed plan from plan mode to TODO task files
allowed-tools: ["Bash", "Write", "Read", "Glob"]
model: claude-3-5-sonnet-20241022
argument-hint: <task-name>
---

# Plan to TODO Conversion Protocol

**Goal**: Convert reviewed plan from Claude Code plan mode to `TODO/<task>/` structure.

## Input Parsing

`$1` = task_name

- Use **hyphens (-)** instead of spaces
- Examples: `auth-system`, `deploy-pipeline`, `hook-refactor`

## Step 1: Detect Plan File

Find the **most recently modified** `.md` file in `~/.claude/plans/` directory:

```bash
PLAN_FILE=$(ls -t ~/.claude/plans/*.md 2>/dev/null | head -1)
```

**If file not found**:

```
❌ Plan file not found.

Please complete planning in plan mode first:
1. Enter plan mode in Claude Code
2. Complete plan creation and review
3. Run /do-todo <task-name>
```

## Step 2: Read and Analyze Plan File

Read the plan file and extract the following elements:

- **Title**: First `#` heading
- **Overview**: Paragraph after title
- **Steps**: `### Step N:` or `### Phase N:` patterns
- **Files to modify**: File path patterns (`path/to/file`)

## Step 3: Scaffolding

```bash
mkdir -p TODO/$1
```

## Step 4: Artifact Generation

Generate **all** of the following files:

### A. TODO/$1/PLAN.md

Structure based on plan file content:

```markdown
# $1 Implementation Plan

## Overview

{Overview section from plan file}

## Goals

- [ ] {Goal derived from plan 1}
- [ ] {Goal derived from plan 2}

## Implementation Phases

### Phase 1: {Phase name}

- Task file: 01.md
- Summary

### Phase 2: {Phase name}

- Task file: 02.md
- Summary

## Affected Files

- `path/to/file` - Reason for change

## Original Plan File

- Path: {PLAN_FILE path}
- Modified: {file modification time}
```

### B. TODO/$1/checklist.md

Derive checklist items from each step in the plan:

```markdown
# $1 Quality Checklist

## Implementation Requirements

- [ ] {Step 1 completion criteria}
- [ ] {Step 2 completion criteria}
- [ ] ...

## Code Quality

- [ ] Lint passed
- [ ] Tests passed
- [ ] Type check passed

## Verification

- [ ] Manual testing completed
- [ ] Edge cases handled
```

### C. TODO/$1/progress.md

```markdown
# $1 Progress

## Current Status: 🟡 Planning Completed

### Timeline

- [{current date/time}] Plan converted from: {PLAN_FILE name}

### Task Status

| Task  | Status     | Completed At |
| ----- | ---------- | ------------ |
| 01.md | ⏳ Pending | -            |
| 02.md | ⏳ Pending | -            |
| ...   | ...        | ...          |

### Completion Rate

- Checklist: 0/{total items} (0%)
```

### D. TODO/$1/01.md, 02.md, ... (Task Files)

Convert each Step/Phase from the plan to separate task files:

```markdown
# Task 01: {Step title}

## Goal

{Extracted from Step description}

## Detailed Instructions

1. {Specific task extracted from Step content}
2. ...

## Expected File Changes

- `path/to/file` - {Change description}

## Completion Criteria

- [ ] {Completion condition for this task}

## Notes

- Source: Step N from {PLAN_FILE}
```

## Step 5: Conclusion

```
✅ Plan converted to TODO structure.

📁 TODO/$1/
├── PLAN.md         - Implementation plan
├── checklist.md    - Quality checklist ({N} items)
├── progress.md     - Progress tracking
├── 01.md           - {Task 1 title}
├── 02.md           - {Task 2 title}
└── ...

Original Plan: {PLAN_FILE}

Next commands:
  /do-task $1       - Start tasks
  /do-progress $1   - Check progress
```
