---
description: Calculate and visually display progress based on checklist.md
allowed-tools: ["Bash", "Read", "Glob"]
model: claude-3-5-sonnet-20241022
argument-hint: [feature-name] [--all]
---

# Progress Dashboard Protocol

**Goal**: Analyze and visually display feature progress based on checklist.md.

## Input Parsing

- `$1` (optional): Check progress of specific feature
- `--all`: Summary of all active features

If neither $1 nor --all is provided, use the most recently modified TODO directory.

## Execution Steps

### 1. Identify Target

```bash
# Specific feature
ls TODO/$1/

# Or all features
ls -d TODO/*/
```

### 2. Checklist Analysis

Read each feature's `checklist.md` and calculate:

```
Total items: Count of `- [ ]` or `- [x]`
Completed items: Count of `- [x]` pattern
Completion rate: (Completed / Total) × 100
```

### 3. Progress Analysis

Read `progress.md` and extract:

- Last activity time
- Last task content
- Timeline summary

### 4. Visual Output

#### Single Feature:

```
╔══════════════════════════════════════════════════════════════╗
║  📊 {feature_name} Progress                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Completion: {percentage}%                                   ║
║  ████████████░░░░░░░░ {completed}/{total} items             ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  📋 Checklist Details                                        ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Functional Requirements                                  ║
║     [x] Requirement 1                                        ║
║     [x] Requirement 2                                        ║
║     [ ] Requirement 3  ← Next task                           ║
║                                                              ║
║  🔧 Code Quality                                             ║
║     [ ] Lint passed                                          ║
║     [ ] Tests passed                                         ║
╠══════════════════════════════════════════════════════════════╣
║  📅 Recent Activity                                          ║
╠══════════════════════════════════════════════════════════════╣
║  {timestamp} - {last_action}                                 ║
║  {timestamp} - {previous_action}                             ║
╠══════════════════════════════════════════════════════════════╣
║  ⏭️  Next Steps                                               ║
╠══════════════════════════════════════════════════════════════╣
║  /do-task {feature_name}    - Execute next task             ║
║  /do-commit {feature_name}  - Commit changes                ║
╚══════════════════════════════════════════════════════════════╝
```

#### All Features Summary (--all):

```
╔══════════════════════════════════════════════════════════════╗
║  📊 Project-wide Progress                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Feature              Progress     Status    Last Activity   ║
║  ─────────────────────────────────────────────────────────── ║
║  auth-system        ████████░░  80%  🟢   2 min ago         ║
║  user-dashboard     ██████░░░░  60%  🟡   1 hour ago        ║
║  payment-gateway    ██░░░░░░░░  20%  🔴   3 days ago        ║
║  notification       ░░░░░░░░░░   0%  ⚪   Planned           ║
╠══════════════════════════════════════════════════════════════╣
║  📈 Statistics                                               ║
║  Total: 4 | Completed: 0 | In Progress: 3 | Pending: 1     ║
║  Overall Completion: 40%                                     ║
╚══════════════════════════════════════════════════════════════╝
```

### 5. Status Icon Rules

| Completion | Status      | Icon |
| ---------- | ----------- | ---- |
| 100%       | Complete    | ✅   |
| 70-99%     | Almost Done | 🟢   |
| 30-69%     | In Progress | 🟡   |
| 1-29%      | Early Stage | 🔴   |
| 0%         | Not Started | ⚪   |

### 6. Progress Bar Generation

Based on 10 blocks:

```
0%:   ░░░░░░░░░░
20%:  ██░░░░░░░░
50%:  █████░░░░░
80%:  ████████░░
100%: ██████████
```

### 7. Recommended Next Actions

- **0%**: `/do-task {feature}` - Start work
- **1-99%**: `/do-task {feature}` - Continue work
- **100%**: `/do-commit {feature}` then `/do-deploy`

## Error Handling

When TODO directory doesn't exist:

```
📭 No active features found.

To start a new feature:
  /do-plan <feature-name>
```
