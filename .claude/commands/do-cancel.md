---
description: Cancel current do-* workflow session
allowed-tools: ["Bash", "Read"]
model: claude-sonnet-4-5-20250929
---

# Cancel Session

## Step 1: Check Session

Check if `.claude/.do-session` file exists.

### If file exists:
1. Read the file and parse JSON
2. Display session info:
```
Active session found:
- Feature: {feature}
- Started: {started_at}
- Phase: {phase}
```
3. Ask: "Cancel this session? (yes/no)"
4. **STOP and WAIT for user response.**
5. If user says yes:
   - Delete `.claude/.do-session` file
   - Report: "Session cancelled."
6. If user says no:
   - Report: "Session kept active."

### If file does not exist:
Report: "No active session found."
