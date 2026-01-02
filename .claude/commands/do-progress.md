---
description: Calculate and visually display progress based on checklist.md
allowed-tools: ["Bash", "Read", "Glob"]
model: claude-sonnet-4-5-20250929
---

# Progress Dashboard

## Steps

### 1. Read Session & Target
1. Read `.claude/.do-session` (extract `feature`). Exit if missing.
2. `ls TODO/{feature}/`

### 2. Analyze
1. **Checklist**: Count total items vs completed items (`- [x]`).
2. **Tasks**: Read `progress.md` for last activity.

### 3. Report
Display simple progress summary:

```
{feature} Progress: {percent}% ({done}/{total})

Checklist:
  Functional: [x] done [ ] pending
  Quality:    [ ] passed

Recent: {time} - {action}
Next: /do-task | /do-commit
```

## Status Icons (Optional)
- 100%: ✅ Complete
- >0%:  🟡 In Progress
- 0%:   ⚪ Planned

## Progress Bar
Simple text bar: `[████░░░░░░]` (10 blocks)

