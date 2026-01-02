# **Claude Code 자율 개발 파이프라인 구축 명세서**

## **1. 개요 및 의도 (Overview & Intent)**

### **배경**

본 문서는 소프트웨어 개발 시 발생하는 반복적인 "계획-실행-검증" 과정을 Claude Code CLI 기능을 활용하여 자동화하기 위한 설계 명세서입니다. 기존의 수동 워크플로우(PLAN.md 작성, progress.md 갱신, checklist.md 검증)를 시스템 레벨에서 강제하고 자동화하여 개발자의 인지 부하를 줄이고 코드 품질을 보장하는 것을 목적으로 합니다.

### **핵심 아키텍처: 상태 기반 에이전트 (Stateful Agent)**

이 파이프라인은 Claude의 "기억(Context Window)"에 의존하지 않고, **파일 시스템을 영구적인 상태 저장소**로 사용합니다.

1. **Plan First**: 복잡한 작업은 반드시 TODO/ 디렉토리에 계획을 수립해야 합니다.
2. **State Preservation**: 모든 진행 상황은 progress.md에 기록되어 세션이 끊겨도 복구 가능합니다.
3. **Quality Gate**: 작업 종료 시 checklist.md가 완료되지 않으면 종료를 차단합니다.

## **2. 디렉토리 구조 (Directory Structure)**

로컬 환경에 아래와 같은 폴더 구조가 생성되어야 합니다.

```
~/.claude/                  # Claude 글로벌 설정 루트
├── settings.json           # 글로벌 설정 및 훅 연결
├── CLAUDE.md               # 글로벌 워크플로우 규칙
├── commands/               # 커스텀 슬래시 커맨드 저장소
│   ├── plan-feature.md     # 계획 수립 커맨드
│   └── execute-task.md     # 작업 실행 커맨드 (Auto-Resume 기능 포함)
└── hooks/                  # 이벤트 기반 파이썬 스크립트
    ├── gatekeeper.py       # UserPromptSubmit (복잡도 판단)
    └── quality_gate.py     # Stop (품질 검증)

./TODO/                     # (프로젝트 루트) 작업 관리 디렉토리
./CLAUDE.md                 # (프로젝트 루트) 프로젝트별 기술 관례
```

## **3. 구성 파일 상세 (Configuration Files)**

아래의 각 파일 내용을 지정된 경로에 생성하십시오.

### **3.1. 글로벌 설정**

- File Path: `~/.claude/settings.json`
- Description: 커맨드와 훅 스크립트를 Claude Code 엔진에 등록합니다.

```json
{
  "auto_compact": true,
  "history_file_path": "~/.claude/history.json",
  "commands": [
    {
      "name": "plan-feature",
      "file": "~/.claude/commands/plan-feature.md",
      "description": "기능 구현을 위한 계획 수립 및 디렉토리 스캐폴딩 자동화"
    },
    {
      "name": "execute-task",
      "file": "~/.claude/commands/execute-task.md",
      "description": "특정 기능(Feature)의 진행 상황을 파악하고 다음 작업을 자동으로 이어서 실행"
    }
  ],
  "hooks": {
    "UserPromptSubmit": "python3 ~/.claude/hooks/gatekeeper.py",
    "Stop": "python3 ~/.claude/hooks/quality_gate.py"
  }
}
```

### **3.2. 글로벌 컨텍스트 (워크플로우 규칙)**

- File Path: `~/.claude/CLAUDE.md`
- Description: 모든 프로젝트에 공통적으로 적용되는 작업 프로세스를 정의합니다.

```markdown
# Global Workflow Rules (~/.claude/CLAUDE.md)

이 파일은 모든 프로젝트에 공통적으로 적용되는 **작업 방식(Process)**을 정의합니다.

## 1. Core Principles (핵심 원칙)

- **Stateful Development**: 모든 작업 상태는 메모리가 아닌 파일 시스템(`TODO/`)에 기록되어야 한다.
- **Plan First**: 복잡한 변경은 반드시 계획(`PLAN.md`)을 먼저 수립한다.
- **Verify Always**: 작업 완료 전 `checklist.md`를 통해 요구사항 충족 여부를 검증한다.

## 2. Directory Structure Convention

모든 기능 개발은 다음과 같은 격리된 구조를 가진다:

- `TODO/<feature_name>/PLAN.md`: 전체 아키텍처 및 계획
- `TODO/<feature_name>/progress.md`: 진행 상황 로그 (자동 업데이트됨)
- `TODO/<feature_name>/checklist.md`: 품질 검증 항목
- `TODO/<feature_name>/XX.md`: (01.md, 02.md...) 세부 작업 단위

## 3. Communication Style

- **Concise**: 불필요한 서두를 생략하고 핵심만 전달한다.
- **File-Driven**: "기억해줘" 대신 "파일에 기록해"를 기본으로 한다.
```

### **3.3. 커스텀 커맨드: 계획 수립**

- File Path: `~/.claude/commands/plan-feature.md`
- Description: 기능명을 입력받아 필요한 파일 구조(PLAN, checklist, progress)를 자동으로 생성합니다.

````markdown
---
description: 기능 구현을 위한 계획 수립 및 디렉토리 스캐폴딩 자동화
allowed-tools: ["Bash", "Write", "Read"]
model: claude-3-5-sonnet-20241022
argument-hint: [feature_name]
---

# Feature Planning Protocol

**목표**: `$ARGUMENTS` 기능을 위한 상세 구현 계획을 수립하고 작업 환경을 구성하십시오.

## Context Loading

1. 프로젝트 규칙 참조: `@CLAUDE.md` (기술 스택 확인)
2. 현재 Git 상태 확인: `!git status`

## Execution Steps

### 1. Analysis (Thinking)

사용자의 요구사항(`$ARGUMENTS`)을 분석하고, 구현을 위해 필요한 파일 변경과 로직을 생각하십시오.

### 2. Scaffolding (Action)

다음 쉘 명령어를 실행하여 작업 공간을 만드십시오:

```bash
mkdir -p TODO/$ARGUMENTS
```
````

### **3. Artifact Generation (Documentation)**

다음 파일들을 생성하십시오. (반드시 생성해야 합니다):

**A. TODO/$ARGUMENTS/PLAN.md**

- 기능의 개요 및 목표
- 구현 단계 (Step-by-Step)
- 영향받는 기존 파일 목록

**B. TODO/$ARGUMENTS/checklist.md**

- [ ] 기능 요구사항 1
- [ ] 기능 요구사항 2
- [ ] npm run lint 통과
- [ ] npm run test 통과

**C. TODO/$ARGUMENTS/progress.md**

- 초기 상태 메시지: "Planning Completed. Ready to start." (날짜 포함)

### **4. Conclusion**

계획 수립이 완료되었음을 알리고, 다음 커맨드로 작업을 시작할 수 있음을 안내하십시오:

```
"계획이 수립되었습니다. /execute-task $ARGUMENTS를 통해 작업을 시작할 수 있습니다."
```

### 3.4. 커스텀 커맨드: 작업 실행 (Auto-Resume)

**File Path:** `~/.claude/commands/execute-task.md`
**Description:** 기능 폴더를 지정하면, 진행 상태를 스스로 파악하여 다음 작업을 자동으로 수행합니다.

```markdown
---
description: 특정 기능(Feature)의 진행 상황을 파악하고 다음 작업을 자동으로 이어서 실행
allowed-tools: ["Bash", "Write", "Read", "Edit", "Ls"]
model: claude-3-5-sonnet-20241022
argument-hint: [feature_name]
---

# Auto-Resume Task Execution Protocol

**Target**: `TODO/$ARGUMENTS` 디렉토리의 잔여 작업을 자동으로 식별하고 실행합니다.

## 1. Context Loading (State Check)

작업 수행을 위해 다음 문맥을 로드합니다:

- **Project Rules**: `@CLAUDE.md` (코딩 컨벤션)
- **Feature Plan**: `@TODO/$ARGUMENTS/PLAN.md` (전체 계획)
- **Progress Log**: `@TODO/$ARGUMENTS/progress.md` (현재 진행 상태)

## 2. Next Task Identification (Reasoning)

**스스로 판단하여 다음 작업을 결정하십시오:**

1. `ls TODO/$ARGUMENTS` 명령을 실행하여 해당 폴더 내의 파일 목록을 확인하십시오.
2. `progress.md`의 기록을 분석하여 이미 완료된 작업(`[x]` 또는 `Completed`)을 파악하십시오.
3. 숫자 순서상 **그 다음으로 진행해야 할 작업 파일(예: `02.md`)**을 찾아 `Read` 도구로 내용을 읽으십시오.
   - _예시: `01.md`가 완료되었다면 `02.md`를 읽고 실행._
   - _만약 다음 번호의 파일이 없다면, `PLAN.md`를 참조하여 다음 단계의 파일을 생성해야 하는지, 아니면 모든 작업이 완료되었는지 사용자에게 알리십시오._

## 3. Execution (Implementation)

식별된 작업 파일의 지시사항에 따라 코드를 작성하거나 수정하십시오.

- **Rule**: 코드를 수정한 후에는 반드시 `CLAUDE.md`에 정의된 테스트나 린트(`npm run lint` 등)를 실행하여 정합성을 검증해야 합니다.

## 4. State Update (Logging)

작업이 성공적으로 완료되면 `TODO/$ARGUMENTS/progress.md`에 결과를 기록하십시오.

- 형식: `- [YYYY-MM-DD HH:mm] {작업파일명} Completed: {간략한 구현 내용}`
- **안내**: 사용자에게 이번에 수행한 작업과, 다음에 수행할 작업이 무엇인지(혹은 끝났는지) 알려주십시오.
```

## **4. 훅(Hooks) 스크립트**

아래 Python 스크립트들은 반드시 실행 권한(chmod +x)이 필요합니다.

### **4.1. Gatekeeper (복잡도 판단)**

- File Path: `~/.claude/hooks/gatekeeper.py`
- Description: 사용자의 입력이 복잡할 경우 /plan-feature 사용을 권장합니다.

```python
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
        print(f"n[Gatekeeper] 감지된 작업 복잡도가 높습니다.", file=sys.stderr)
        print(f"[Gatekeeper] 체계적인 관리를 위해 다음 커맨드 사용을 권장합니다:", file=sys.stderr)
        print(f"[Gatekeeper] >> /plan-feature <기능명>", file=sys.stderr)
        print(f"[Gatekeeper] 그대로 진행하려면 엔터를 누르세요...", file=sys.stderr)
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### **4.2. Quality Gate (품질 검증)**

- File Path: `~/.claude/hooks/quality_gate.py`
- Description: 작업 종료 시도 시 체크리스트 미완료 항목을 감지하여 차단합니다.

```python
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
    unchecked_pattern = re.compile(r'-s*[s*]')
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
        print(f"n[Quality Gate] ⛔ 작업 종료 불가!", file=sys.stderr)
        print(f"[Quality Gate] {checklist_path} 에 완료되지 않은 항목이 {remaining}개 있습니다.", file=sys.stderr)
        print("체크리스트 검증 실패: 아직 완료되지 않은 항목이 있습니다. checklist.md를 확인하고 작업을 마무리해주세요.")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

## **5. 프로젝트 예시 파일 (Project Context)**

이 파일은 각 프로젝트의 루트 디렉토리에 위치해야 합니다.

- File Path: `./CLAUDE.md` (프로젝트 루트)
- Description: 해당 프로젝트의 기술 스택과 실행 방법을 정의합니다.

```markdown
# Project Context (./CLAUDE.md)

이 파일은 현재 프로젝트의 **기술적 관례(Tech Stack & Conventions)**를 정의합니다.

## 1. Tech Stack

- **Language**: TypeScript 5.0+
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Testing**: Vitest

## 2. Coding Conventions

- 모든 컴포넌트는 Functional Component로 작성.
- Props Interface는 컴포넌트 파일 내 상단에 정의.

## 3. Commands

- **Build**: `npm run build`
- **Lint**: `npm run lint`
- **Test**: `npm run test`
```
