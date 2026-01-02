#!/usr/bin/env python3
import sys
import os
import glob
import re

"""
Hook: Stop
Role: Quality Gate
Description: 대화 종료 시 checklist.md의 모든 항목이 체크되었는지 검증합니다.
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
        print(f"\n[Quality Gate] ⛔ 작업 종료 불가!", file=sys.stderr)
        print(f"[Quality Gate] {checklist_path} 에 완료되지 않은 항목이 {remaining}개 있습니다.", file=sys.stderr)
        print("체크리스트 검증 실패: 아직 완료되지 않은 항목이 있습니다. checklist.md를 확인하고 작업을 마무리해주세요.")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
