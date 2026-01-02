#!/usr/bin/env python3
import sys
import os
import glob
from datetime import datetime

"""
Hook: PostToolUse
Role: Auto Logger
Description: Automatically logs to progress.md when file modifications (Write/Edit) occur.
"""

def find_latest_todo_dir():
    todo_dirs = glob.glob("TODO/*/")
    if not todo_dirs:
        return None
    return max(todo_dirs, key=os.path.getmtime)

def main():
    # Handle stdin (prevent blocking)
    if not sys.stdin.isatty():
        _ = sys.stdin.read()

    todo_dir = find_latest_todo_dir()
    if todo_dir:
        progress_path = os.path.join(todo_dir, "progress.md")
        if os.path.exists(progress_path):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(progress_path, "a") as f:
                    f.write(f"\n- [{timestamp}] Tool action executed (Auto-logged).")
            except Exception:
                pass

    sys.exit(0)

if __name__ == "__main__":
    main()
