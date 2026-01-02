---
description: Calculate and visually display progress based on checklist.md
allowed-tools: ["Bash", "Read", "Glob"]
model: claude-3-5-sonnet-20241022
argument-hint: [feature-name] [--all]
---

# Progress Dashboard

## Input
- `$1`: Specific feature (optional)
- `--all`: All features summary
- No args: Most recently modified TODO directory

## Steps

### 1. Find Target
```bash
ls TODO/$1/          # specific
ls -d TODO/*/        # all
```

### 2. Analyze checklist.md
- Total: Count `- [ ]` + `- [x]`
- Completed: Count `- [x]`
- Rate: Completed / Total × 100

### 3. Read progress.md
Extract last activity, last task, timeline.

### 4. Output Format

**Single Feature:**
```
{feature_name} Progress
Completion: {%} [{bar}] {done}/{total}

Checklist:
  Functional: [x] done [ ] pending ← Next
  Code Quality: [ ] lint [ ] tests

Recent: {time} - {action}
Next: /do-task {name} | /do-commit {name}
```

**All Features (--all):**
```
Feature           Progress   Status  Last Activity
{name}            {bar} {%}  {icon}  {time}

Stats: Total N | Done N | Progress N | Pending N
Overall: {%}
```

### 5. Status Icons
| Rate | Icon | Meaning |
|------|------|---------|
| 100% | ✅ | Complete |
| 70%+ | 🟢 | Almost |
| 30%+ | 🟡 | Working |
| 1%+  | 🔴 | Early |
| 0%   | ⚪ | Planned |

### 6. Progress Bar (10 blocks)
`░`=empty, `█`=filled. Example: 50% → `█████░░░░░`

## No TODO Found
```
No active features. Start: /do-plan <name>
```
