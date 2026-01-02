---
description: Cancel current do-* workflow session
allowed-tools: ["Bash", "Read"]
model: claude-sonnet-4-5-20250929
---

# Cancel Session

## Logic
1. Check `.claude/.do-session`.
2. **If Exists**:
   - Read/Show info (feature, start time).
   - Ask: "Cancel? (yes/no)"
   - **STOP and WAIT for response.**
   - yes: Delete file. Report "Cancelled".
   - no: Report "Active".
3. **If Missing**:
   - Report "No session".
