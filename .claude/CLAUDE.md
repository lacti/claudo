# Global Workflow Rules (~/.claude/CLAUDE.md)

This file defines the **workflow conventions** that apply globally to all projects.

## 1. Core Principles

- **Stateful Development**: All task states must be recorded in the file system (`TODO/`), not in memory.
- **Plan First**: Complex changes must be planned (`PLAN.md`) before implementation.
- **Verify Always**: Verify requirement fulfillment through `checklist.md` before completing work.

## 2. Directory Structure Convention

All feature development follows this isolated structure:

- `TODO/<feature_name>/PLAN.md`: Overall architecture and plan
- `TODO/<feature_name>/progress.md`: Progress log (auto-updated)
- `TODO/<feature_name>/checklist.md`: Quality verification items
- `TODO/<feature_name>/XX.md`: (01.md, 02.md...) Individual task units

## 3. Communication Style

- **Concise**: Skip unnecessary preambles and deliver key points only.
- **File-Driven**: Default to "write it to a file" instead of "remember this".
