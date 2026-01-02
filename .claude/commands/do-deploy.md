---
description: Read deployment instructions (DEPLOY.md) and execute deployment process
allowed-tools: ["Bash", "Read", "Write"]
model: claude-sonnet-4-5-20250929
argument-hint: [environment] [--init]
---

# Deployment Protocol

## Input
- `$1`: Environment (production, staging, dev). Default from DEPLOY.md
- `--init`: Generate DEPLOY.md template

## Steps

### 1. Find DEPLOY.md
Search order: `./DEPLOY.md`, `./deploy/DEPLOY.md`, `./docs/DEPLOY.md`, `./.claude/DEPLOY.md`

### 2. Not Found
```
DEPLOY.md not found. Create at ./DEPLOY.md or run /do-deploy --init
```

### 3. --init: Generate Template
Create DEPLOY.md with: Environments (prod/staging), Pre-requisites, Deployment Steps, Rollback, Post-deploy checklist.

### 4. File Exists → Execute

#### 4.1 Show Info
```
Deploying: {env}, Branch: {branch}, Commit: {hash}
```

#### 4.2 Run Pre-requisites
Execute each command. On failure:
```
Pre-req failed: {step}. Aborted.
```

#### 4.3 Deploy
Execute deployment steps from DEPLOY.md.

#### 4.4 Post-deploy
```
Done! Env: {env}, Time: {time}, Commit: {hash}
Checklist: [ ] health [ ] manual test [ ] logs
```

### 5. Record
Add to progress.md: `- [{now}] Deployed to {env}: {hash}`

## Safety
- Confirm before Production
- Warn if not on main/master
- Block if uncommitted changes
- Only run commands from DEPLOY.md
