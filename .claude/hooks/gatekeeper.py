#!/usr/bin/env python3
import sys
import os

"""
Hook: UserPromptSubmit
Role: Gatekeeper
Description: 사용자의 프롬프트를 분석하여 복잡한 작업인 경우 /plan-feature 사용을 권장합니다.
"""

def analyze_complexity(prompt):
    prompt_len = len(prompt)
    keywords_complex = ['구현', '개발', '만들어', '리팩토링', '변경', 'create', 'implement', 'refactor']
    keywords_simple = ['오타', '수정', 'typo', 'fix', 'explain', '설명']

    if prompt_len < 20 and any(k in prompt.lower() for k in keywords_simple):
        return "simple"

    if prompt.strip().startswith("/"):
        return "command"

    if any(k in prompt.lower() for k in keywords_complex) or prompt_len > 50:
        return "complex"

    return "unknown"

def main():
    try:
        user_prompt = sys.stdin.read().strip()
    except Exception:
        sys.exit(0)

    complexity = analyze_complexity(user_prompt)

    if complexity == "complex":
        print(f"\n[Gatekeeper] 감지된 작업 복잡도가 높습니다.", file=sys.stderr)
        print(f"[Gatekeeper] 체계적인 관리를 위해 다음 커맨드 사용을 권장합니다:", file=sys.stderr)
        print(f"[Gatekeeper] >> /plan-feature <기능명>", file=sys.stderr)
        print(f"[Gatekeeper] 그대로 진행하려면 엔터를 누르세요...", file=sys.stderr)
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
