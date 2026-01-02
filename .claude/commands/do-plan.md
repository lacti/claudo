---
description: Create implementation plan and task files (interactive)
allowed-tools: ["Bash", "Write", "Read", "Glob", "Grep"]
model: claude-3-5-sonnet-20241022
argument-hint: <feature-name>
---

# Feature Planning Protocol (Interactive Mode)

**Goal**: Create a detailed implementation plan through conversation with the user, generating all task files.

## Input Parsing

`$1` = feature_name

- Use **hyphens (-)** instead of spaces
- Examples: `auth-system`, `user-dashboard`, `payment-gateway`

## Step 1: Requirements Gathering (Interactive)

**If only feature name is provided** (`$2` is empty):

Ask the user the following:

```
📋 Planning the $1 feature.

Please provide detailed requirements:
- What functionality is needed?
- What are the main user scenarios?
- Any specific technical constraints to consider?
```

**If detailed requirements are provided**:

- Use the remainder of `$ARGUMENTS` after `$1` as requirements

## Step 2: Context Loading

1. Reference project rules: `@CLAUDE.md` (check tech stack)
2. Check current Git status: `!git status`
3. Search for related existing code

## Step 3: Analysis & Planning

Analyze user requirements and:

- Derive list of files to be changed
- Review integration approach with existing code
- Identify potential risks
- **Split implementation into subtasks** (01, 02, 03...)

## Step 4: Scaffolding

```bash
mkdir -p TODO/$1
```

## Step 5: Artifact Generation

Generate **all** of the following files:

### A. TODO/$1/PLAN.md

```markdown
# $1 Implementation Plan

## Overview

{Requirements summary}

## Goals

- [ ] Goal 1
- [ ] Goal 2

## Implementation Phases

### Phase 1: {Phase name}

- Task file: 01.md
- Summary

### Phase 2: {Phase name}

- Task file: 02.md
- Summary

### Phase N: ...

## Affected Files

- `path/to/file1.ts` - Reason for change

## Technical Considerations

- Dependencies, compatibility, performance, etc.
```

### B. TODO/$1/requirements.md

```markdown
# $1 Requirements Specification

## Original Request

{Full user requirements}

## Analyzed Requirements

1. ...
2. ...

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

### C. TODO/$1/checklist.md

```markdown
# $1 Quality Checklist

## Functional Requirements

- [ ] {Requirement derived item 1}
- [ ] {Requirement derived item 2}
- [ ] ...

## Code Quality

- [ ] Lint passed (npm run lint)
- [ ] Tests passed (npm run test)
- [ ] Type check passed

## Verification

- [ ] Manual testing completed
- [ ] Edge cases handled
```

### D. TODO/$1/progress.md

```markdown
# $1 Progress

## Current Status: 🟡 Planning Completed

### Timeline

- [{current date/time}] Planning Completed. Ready to start.

### Task Status

| Task  | Status     | Completed At |
| ----- | ---------- | ------------ |
| 01.md | ⏳ Pending | -            |
| 02.md | ⏳ Pending | -            |
| ...   | ...        | ...          |

### Completion Rate

- Checklist: 0/{total items} (0%)
```

### E. TODO/$1/01.md, 02.md, ... (Task Files)

**Create a separate task file for each implementation phase:**

```markdown
# Task 01: {Task title}

## Goal

{Specific goal to achieve in this task}

## Detailed Instructions

1. {Specific implementation step 1}
2. {Specific implementation step 2}
3. ...

## Expected File Changes

- `path/to/file.ts` - {Change description}

## Completion Criteria

- [ ] {Completion condition 1}
- [ ] {Completion condition 2}

## Notes

- {Cautions, dependencies, etc.}
```

**Task file writing rules:**

- Each task should be independently executable
- Split appropriately to avoid too much in one task
- Clearly state dependencies on previous tasks

## Step 6: Conclusion

```
✅ Planning completed.

📁 TODO/$1/
├── PLAN.md         - Implementation plan
├── requirements.md - Requirements specification
├── checklist.md    - Quality checklist ({N} items)
├── progress.md     - Progress tracking
├── 01.md           - {Task 1 title}
├── 02.md           - {Task 2 title}
└── ...

Next commands:
  /do-task $1       - Start tasks
  /do-progress $1   - Check progress
```
