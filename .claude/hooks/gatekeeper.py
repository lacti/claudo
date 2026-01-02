#!/usr/bin/env python3
import sys

"""
Hook: UserPromptSubmit
Role: Gatekeeper
Description: Analyzes user prompts and recommends using /do-plan for complex tasks.
"""

def analyze_complexity(prompt):
    prompt_len = len(prompt)
    keywords_complex = ['create', 'implement', 'refactor', 'build', 'develop', 'design', 'restructure']
    keywords_simple = ['typo', 'fix', 'explain', 'describe', 'show', 'list', 'what is']

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
        print("\n[Gatekeeper] High task complexity detected.", file=sys.stderr)
        print("[Gatekeeper] For systematic task management, consider using:", file=sys.stderr)
        print("[Gatekeeper] >> /do-plan <feature-name>", file=sys.stderr)
        print("[Gatekeeper] Press Enter to proceed anyway...", file=sys.stderr)
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
