#!/usr/bin/env python3
import sys
import os
import glob
import re
import json

"""
Hook: Stop
Role: Quality Gate
Description: Verifies all items in checklist.md are checked before conversation ends.
Only active when a do-* workflow session exists (.claude/.do-session) and phase is 'executing'.
"""

def get_session_phase():
    """Get the current session phase. Returns None if no session or phase."""
    session_path = ".claude/.do-session"
    if not os.path.exists(session_path):
        return None
    try:
        with open(session_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("phase")
    except (json.JSONDecodeError, IOError):
        return None

def is_do_session_active():
    """Check if do-* workflow session is active and in executing phase."""
    phase = get_session_phase()
    return phase == "executing"

def find_active_checklist():
    todo_dirs = glob.glob("TODO/*/")
    if not todo_dirs:
        return None
    latest_dir = max(todo_dirs, key=os.path.getmtime)
    checklist_path = os.path.join(latest_dir, "checklist.md")
    if os.path.exists(checklist_path):
        return checklist_path
    return None

def check_quality_gate(checklist_path):
    with open(checklist_path, 'r', encoding='utf-8') as f:
        content = f.read()
    unchecked_pattern = re.compile(r'-\s*\[\s*\]')
    unchecked_items = unchecked_pattern.findall(content)
    if unchecked_items:
        return False, len(unchecked_items)
    return True, 0

def main():
    # Only active when do-* session exists
    if not is_do_session_active():
        sys.exit(0)

    checklist_path = find_active_checklist()
    if not checklist_path:
        sys.exit(0)

    passed, remaining = check_quality_gate(checklist_path)

    if not passed:
        print("\n[Quality Gate] Cannot end session!", file=sys.stderr)
        print(f"[Quality Gate] {checklist_path} has {remaining} incomplete item(s).", file=sys.stderr)
        print("Checklist verification failed: There are still incomplete items. Please review checklist.md and complete remaining tasks.")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
