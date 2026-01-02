---
description: Identify and execute next task automatically, review checklist on completion
allowed-tools: ["Bash", "Write", "Read", "Edit", "Ls"]
model: claude-sonnet-4-5-20250929
argument-hint: <feature-name>
---

# Auto Task Execution

## 0. Update Session Phase
Read `.claude/.do-session` and update `phase` to `"executing"` if it's `"planning"`.
This enables the quality gate hook for checklist verification on session end.

## 1. Load Context
- `@CLAUDE.md` - coding conventions
- `@TODO/$1/PLAN.md` - plan
- `@TODO/$1/progress.md` - current state

## 2. Find Next Task
1. `ls TODO/$1` to list files
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

## 4. All Tasks Done → Checklist Review

### 4.1 Load `@TODO/$1/checklist.md`

### 4.2 Verify Items
Code Quality:
```bash
npm run lint && npm run test && npm run typecheck
```
Functional: Review code against requirements.

### 4.3 Update Checklist
Mark passed items: `- [x] Lint passed`

### 4.4 Fix Incomplete
Loop: fix → verify → repeat until all pass.

### 4.5 Done Report
1. Delete `.claude/.do-session` file
2. Report:
```
All done! Tasks: N, Checklist: M items passed.
Next: /do-commit $1 | /do-deploy
```

## 5. Update Status
In progress: `## Status: 🔵 In Progress (N/M)`
Complete: `## Status: ✅ Complete`, Rate: 100%

## 6. Progress Report
```
Done: {task}
Changes: {list}
Remaining: {count} tasks
Next: /do-task $1 | /do-progress $1
```
