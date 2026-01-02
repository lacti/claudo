---
description: Identify and execute next task automatically, review checklist on completion
allowed-tools: ["Bash", "Write", "Read", "Edit", "Ls"]
model: claude-sonnet-4-5-20250929
---

# Auto Task Execution

## 0. Read Session
1. Read `.claude/.do-session` JSON, extract `feature` field
2. If session not found → show "No active session. Start: /do-plan <name>" and exit
3. Update `phase` to `"executing"` if it's `"planning"`
   This enables the quality gate hook for checklist verification on session end.

## 1. Load Context
- `@CLAUDE.md` - coding conventions
- `@TODO/{feature}/PLAN.md` - plan
- `@TODO/{feature}/progress.md` - current state

## 2. Find Next Task
1. `ls TODO/{feature}` to list files
2. Check progress.md for completed tasks (✅)
3. Pick next numbered task file (01.md → 02.md → ...)

## 3. Execute Task
If tasks remain:
1. Read task file
2. Implement according to instructions
3. Run tests/lint per CLAUDE.md
4. Update progress.md:
   - Timeline: `- [{now}] NN.md Done: {summary}`
   - Table: `| NN.md | ✅ | {time} |`

## 4. All Tasks Done → Session Complete

### 4.1 Verify Final Review Completed
The last task is always "Final Review" task.
It includes checklist verification and code review.

### 4.2 Check Session Status
After Final Review task is done, check if additional implementation is required:
- **Additional work needed**: Keep `.do-session`, guide to `/do-plan {feature}`
- **All complete**: Go to 4.3

### 4.3 Done Report
**Only when all checklist items are `[x]`:**
1. Delete `.claude/.do-session` file
2. Report:
```
All done! Tasks: N, Checklist: M items passed.
Next: /do-commit | /do-deploy
```

### 4.4 Additional Work Detected (from Final Review)
If Final Review task identified issues requiring new implementation:
**DO NOT delete `.do-session`**
Report:
```
Additional implementation required during Final Review.

Issues found:
- {issue 1}
- {issue 2}

Session: Active (not completed)
Next: /do-plan {feature}
```

## 5. Update Status
In progress: `## Status: 🔵 In Progress (N/M)`
Complete: `## Status: ✅ Complete`, Rate: 100%

## 6. Progress Report
```
Done: {task}
Changes: {list}
Remaining: {count} tasks
Next: /do-task | /do-progress
```
