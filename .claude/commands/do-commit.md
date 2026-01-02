---
description: Analyze changes and create git commit automatically
allowed-tools: ["Bash", "Read", "Edit"]
model: claude-3-5-sonnet-20241022
argument-hint: [feature-name] [--amend]
---

# Auto Commit Protocol

**Goal**: Analyze current changes, generate meaningful commit message, and auto-commit.

## Input Parsing

- `$1` (optional): Feature name to associate with
- `--amend` (optional): Amend last commit (use with caution)

## Execution Steps

### 1. Collect Changes

```bash
# Changed files list
git status --porcelain

# Staged changes detail
git diff --cached

# Unstaged changes
git diff

# New file contents (untracked)
git status --porcelain | grep "^??" | cut -c4-
```

### 2. Analyze Changes

- **Change type classification**: feat, fix, refactor, docs, test, chore, style
- **Scope**: Which modules/components were changed
- **Purpose**: Why this change was needed

### 3. Generate Commit Message

Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Example:**

```
feat(auth): Implement JWT-based authentication system

- Add login/logout API endpoints
- Implement refresh token logic
- Apply authentication middleware

Related: TODO/auth-system
```

### 4. User Confirmation

```
📝 Commit Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type: {type}
Scope: {scope}
Subject: {subject}

Changed files:
  M  src/auth/login.ts
  A  src/auth/token.ts
  D  src/old-auth.ts

Message:
{full commit message}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceed with commit? (continuing)
```

### 5. Execute Commit

```bash
git add -A
git commit -m "{commit message}"
```

**With --amend option:**

```bash
git commit --amend -m "{amended commit message}"
```

### 6. If feature_name is specified

Record commit info in `TODO/$1/progress.md`:

```markdown
- [{current date/time}] Commit: {first 7 chars of hash} - {commit subject}
```

### 7. Result Report

```
✅ Commit completed

Commit hash: {hash}
Branch: {current_branch}
Message: {subject}

Change statistics:
  {n} files changed, {insertions} insertions(+), {deletions} deletions(-)

Next steps:
  git push origin {branch}  # Push to remote
  /do-deploy                # Run deployment
```

## Safety Rules

- **Never use --force option**
- **Warn before using --amend on main/master branch**
- **Warn and exclude sensitive files (.env, credentials, etc.)**
