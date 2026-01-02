---
description: Identify and execute next task automatically, review checklist on completion
allowed-tools: ["Bash", "Write", "Read", "Edit", "Ls"]
model: claude-sonnet-4-5-20250929
---

# Auto Task Execution

## 0. Session & Context
1. Read `.claude/.do-session` (extract `feature`). Exit if missing.
2. Update `phase` to `"executing"` if needed.
3. Load: `@CLAUDE.md`, `@TODO/{feature}/PLAN.md`, `@TODO/{feature}/progress.md`

## 1. Find Next Task
1. `ls TODO/{feature}`
2. Check `progress.md` for completed tasks.
3. Pick next numbered task (01 → 02...).

## 2. Execute Task
If task remains:
1. Read task file.
2. Implement.
3. Run tests/lint.
4. Update `progress.md`:
   - Timeline: `- [{now}] NN.md Done: {summary}`
   - Table: `| NN.md | ✅ | {time} |`
5. Report: "Done: {task}. Next: /do-task"

## 3. Session Complete (All Tasks Done)
Last task is "Final Review" (checklist verification).

### 3.1 Check Status
- **Assignments needed?** (Read Final Review notes) -> Keep session.
- **All nice?** (Checklist complete) -> Done.

### 3.2 Report
**If Done:**
1. Delete `.claude/.do-session`
2. Report:
```
All done! Tasks: N, Checklist passed.
Next: /do-commit | /do-deploy
```

**If Work Remains:**
1. Keep `.do-session`
2. Report:
```
Additional implementation required.
Issues: ...
Next: /do-plan {feature}
```

## 4. Progress Update
- Update `## Status` in `progress.md`:
  - 🔵 In Progress (N/M)
  - ✅ Complete (if done)

