---
description: Read deployment instructions (DEPLOY.md) and execute deployment process
allowed-tools: ["Bash", "Read", "Write"]
model: claude-sonnet-4-5-20250929
argument-hint: [environment] [--init]
---

# Deployment Protocol

## Input
- `$1`: Env (prod/staging/dev). Default from DEPLOY.md.
- `--init`: Generate DEPLOY.md.

## Steps

### 1. Find DEPLOY.md
Search: `./DEPLOY.md` or `.claude/DEPLOY.md`.
If missing: Prompt to create (or run with --init).

### 2. --init (if requested)
Create `DEPLOY.md`: Envs, Pre-reqs, Steps, Rollback, Checklist.

### 3. Execution
1. **Load**: `DEPLOY.md`
2. **Pre-reqs**: Run commands. Abort if fail.
3. **Deploy**: Execute steps.
4. **Post-deploy**: Verify.

### 4. Report & Record
```
Done! Env: {env}, Commit: {hash}
Checklist: [ ] health [ ] manual
```
- Add to `progress.md`: `- [{now}] Deployed to {env}: {hash}`

## Safety
- Confirm PROD.
- Warn if dirty git status.
