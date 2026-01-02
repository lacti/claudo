#!/usr/bin/env python3
import sys
import os
import glob
import re

"""
Hook: Stop
Role: Quality Gate
Description: Verifies all items in checklist.md are checked before conversation ends.
"""

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
    checklist_path = find_active_checklist()
    if not checklist_path:
        sys.exit(0)

    passed, remaining = check_quality_gate(checklist_path)

    if not passed:
        print(f"\n[Quality Gate] ⛔ Cannot end session!", file=sys.stderr)
        print(f"[Quality Gate] {checklist_path} has {remaining} incomplete item(s).", file=sys.stderr)
        print("Checklist verification failed: There are still incomplete items. Please review checklist.md and complete remaining tasks.")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
