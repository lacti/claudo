---
description: Analyze changes and create git commit automatically
allowed-tools: ["Bash", "Read", "Edit"]
model: claude-sonnet-4-5-20250929
argument-hint: [feature-name] [--amend]
---

# Auto Commit

## Input
- `$1`: Feature name (optional)
- `--amend`: Amend last commit

## Steps

### 1. Changes & Context
1. `git status --porcelain`
2. `git diff --cached` / `git diff`
3. Identify Type/Scope/Purpose.

### 2. Message
Format: `<type>(<scope>): <subject>` + body + footer
Example: `feat(auth): Add JWT authentication`

### 3. Review & Confirm
Show: Type, Scope, Files, Message.
Ask: "Proceed?"

### 4. Commit
```bash
git add -A && git commit -m "{message}"
# Or with --amend if requested
```

### 5. Record
1. Resolve Feature: `$1` or from `.claude/.do-session`.
2. Update `progress.md`: `- [{now}] Commit: {hash} - {subject}`
   (Skip if no feature context)

### 6. Report
```
Done! Hash: {hash}, Branch: {branch}
Stats: N files, +X -Y
Next: git push | /do-deploy
```

## Safety
- No `--force`.
- Warn `--amend` on main.
- Exclude secrets.
