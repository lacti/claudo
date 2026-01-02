---
description: Calculate and visually display progress based on checklist.md
allowed-tools: ["Bash", "Read", "Glob"]
model: claude-sonnet-4-5-20250929
---

# Progress Dashboard

## Steps

### 1. Resolve Feature Name

1. Read `.claude/.do-session` JSON, extract `feature` field
2. If session not found → show "No active session. Start: /do-plan <request>" and exit

### 2. Find Target

```bash
ls TODO/{feature}/   # from $1 or .do-session
```

### 3. Analyze checklist.md

- Total: Count `- [ ]` + `- [x]`
- Completed: Count `- [x]`
- Rate: Completed / Total × 100

### 4. Read progress.md

Extract last activity, last task, timeline.

### 5. Output Format

```
{feature_name} Progress
Completion: {%} [{bar}] {done}/{total}

Checklist:
  Functional: [x] done [ ] pending ← Next
  Code Quality: [ ] lint [ ] tests

Recent: {time} - {action}
Next: /do-task | /do-commit
```

### 6. Status Icons

| Rate | Icon | Meaning  |
| ---- | ---- | -------- |
| 100% | ✅   | Complete |
| 70%+ | 🟢   | Almost   |
| 30%+ | 🟡   | Working  |
| 1%+  | 🔴   | Early    |
| 0%   | ⚪   | Planned  |

### 7. Progress Bar (10 blocks)

`░`=empty, `█`=filled. Example: 50% → `█████░░░░░`

## No TODO Found

```
No active features. Start: /do-plan <name>
```
