---
description: Read deployment instructions (DEPLOY.md) and execute deployment process
allowed-tools: ["Bash", "Read", "Write"]
model: claude-3-5-sonnet-20241022
argument-hint: [environment] [--init]
---

# Deployment Protocol

**Goal**: Check project deployment instruction file and execute deployment according to defined process.

## Input Parsing

- `$1` (optional): Specify deployment environment (production, staging, dev, etc.)
- `--init`: Generate DEPLOY.md template
- If no environment specified, use default environment from DEPLOY.md

## Execution Steps

### 1. Check Deployment Instruction File

Search for deployment instruction file in this order:

```
1. ./DEPLOY.md (project root)
2. ./deploy/DEPLOY.md
3. ./docs/DEPLOY.md
4. ./.claude/DEPLOY.md
```

### 2. If File Does Not Exist

**Stop immediately** and output the following message:

```
⚠️  Deployment instruction file not found.

A DEPLOY.md file is required to run deployment.
Please create the file in one of these locations:

  📄 ./DEPLOY.md (recommended)
  📄 ./deploy/DEPLOY.md
  📄 ./.claude/DEPLOY.md

Would you like to generate a DEPLOY.md template?
  /do-deploy --init
```

### 3. If --init Option Provided

Generate DEPLOY.md template:

```markdown
# Deployment Guide

## Environment Configuration

### Production

- **URL**: https://example.com
- **Branch**: main
- **Auto-deploy**: false

### Staging

- **URL**: https://staging.example.com
- **Branch**: develop
- **Auto-deploy**: true

## Pre-requisites

Verify the following before deployment:

- [ ] All tests passed (`npm run test`)
- [ ] Lint check passed (`npm run lint`)
- [ ] Build successful (`npm run build`)
- [ ] Environment variables configured

## Deployment Steps

### 1. Build

\`\`\`bash
npm run build
\`\`\`

### 2. Test

\`\`\`bash
npm run test
\`\`\`

### 3. Execute Deployment

\`\`\`bash

# Production

npm run deploy:prod

# Staging

npm run deploy:staging
\`\`\`

## Rollback Procedure

If issues occur:
\`\`\`bash

# Rollback to previous version

npm run rollback
\`\`\`

## Post-deployment Verification

- [ ] Verify health check endpoint
- [ ] Manual test of key features
- [ ] Monitor error logs
```

### 4. If File Exists

Read DEPLOY.md file and perform the following:

#### 4.1 Environment Check

```
🚀 Preparing Deployment

Environment: {environment}
Branch: {current_branch}
Latest commit: {commit_hash} - {commit_message}

Target: {target_url}
```

#### 4.2 Pre-requisite Check

Execute commands defined in "Pre-requisites" section of DEPLOY.md sequentially:

```bash
# Example
npm run test
npm run lint
npm run build
```

**If any fail, stop immediately:**

```
❌ Pre-requisite check failed

Failed step: {step_name}
Error message: {error_message}

Deployment aborted. Please fix the above error and try again.
```

#### 4.3 Execute Deployment

Execute commands defined in "Deployment Steps" section of DEPLOY.md:

```
📦 Deployment in progress...

[1/3] Building... ✅
[2/3] Running tests... ✅
[3/3] Deploying... ✅
```

#### 4.4 Post-deployment Verification

Display checklist from "Post-deployment Verification" section of DEPLOY.md:

```
✅ Deployment Complete!

Post-deployment checklist:
- [ ] Verify health check endpoint
- [ ] Manual test of key features
- [ ] Monitor error logs

Deployment info:
  Environment: {environment}
  Time: {timestamp}
  Commit: {commit_hash}
  Version: {version}
```

### 5. Deployment Record

On successful deployment, record in active TODO directory's progress.md:

```markdown
- [{current date/time}] 🚀 Deployed to {environment}: {commit_hash}
```

## Safety Rules

- **Always show confirmation prompt before Production deployment**
- **Warn if not on main/master branch**
- **Block deployment if uncommitted changes exist**
- **Never execute commands not defined in DEPLOY.md**
