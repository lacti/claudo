---
description: Analyze changes and create git commit automatically
allowed-tools: ["Bash", "Read", "Edit"]
model: claude-sonnet-4-5-20250929
argument-hint: [feature-name] [--amend]
---

# Auto Commit

## Input
- `$1`: Feature name (optional)
- `--amend`: Amend last commit (caution)

## Steps

### 1. Collect Changes
```bash
git status --porcelain
git diff --cached
git diff
```

### 2. Analyze
- Type: feat, fix, refactor, docs, test, chore, style
- Scope: affected modules
- Purpose: why changed

### 3. Generate Message
Format: `<type>(<scope>): <subject>` + body + footer

Example:
```
feat(auth): Add JWT authentication

- Login/logout endpoints
- Refresh token logic

Related: TODO/auth-system
```

### 4. Confirm
```
Type: {type}, Scope: {scope}
Files: M/A/D list
Message: {full message}
Proceed?
```

### 5. Commit
```bash
git add -A && git commit -m "{message}"
```
With --amend: `git commit --amend -m "{message}"`

### 6. Record (if $1)
Add to `TODO/$1/progress.md`: `- [{now}] Commit: {hash} - {subject}`

### 7. Report
```
Done! Hash: {hash}, Branch: {branch}
Stats: N files, +X -Y
Next: git push | /do-deploy
```

## Safety
- Never --force
- Warn --amend on main/master
- Exclude .env, credentials
