#!/usr/bin/env python3
import sys
import os
import glob
from datetime import datetime

"""
Hook: PostToolUse
Role: Auto Logger
Description: 파일 수정(Write/Edit)이 발생하면 progress.md에 자동으로 로그를 남깁니다.
"""

def find_latest_todo_dir():
    todo_dirs = glob.glob("TODO/*/")
    if not todo_dirs:
        return None
    return max(todo_dirs, key=os.path.getmtime)

def main():
    # stdin 처리 (Blocking 방지)
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
