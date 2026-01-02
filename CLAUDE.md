# Claude Code Extensions 개발 가이드

## 개발 환경 설정

이 프로젝트에서 Claude Code를 실행하면 `.claude/settings.json`의 설정이 적용됩니다.
개발 중인 hooks는 `$CLAUDE_PROJECT_DIR/.claude/hooks/` 경로를 사용합니다.

## 핵심 규칙

### 1. 경로 규칙

**개발 환경 (이 프로젝트)**

```
$CLAUDE_PROJECT_DIR/.claude/hooks/xxx.py
$CLAUDE_PROJECT_DIR/.claude/commands/xxx.md
```

**운영 환경 (~/.claude/)**

```
~/.claude/hooks/xxx.py
~/.claude/commands/xxx.md
```

- 개발 시: `$CLAUDE_PROJECT_DIR` 사용
- 배포 시: `deploy.sh`가 자동으로 `~/.claude`로 변환

### 2. settings.json 수정 시 주의

프로젝트의 `.claude/settings.json`을 수정할 때:

- `commands`, `hooks` 키만 배포 대상
- 다른 키(예: `model`, `mcpServers`)는 배포되지 않음
- 배포 시 기존 `~/.claude/settings.json`의 다른 설정은 유지됨

### 3. Hook 개발 규칙

```python
#!/usr/bin/env python3
import sys

def main():
    # stdin에서 입력 읽기
    input_data = sys.stdin.read()

    # 처리 로직

    # stdout: 사용자에게 표시할 메시지
    # stderr: 로그/경고 메시지
    # exit(0): 성공, exit(1): 차단
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Hook 종류별 입력**

| Hook             | stdin 입력            |
| ---------------- | --------------------- |
| UserPromptSubmit | 사용자 프롬프트       |
| PostToolUse      | 도구 실행 결과 (JSON) |
| Stop             | 세션 정보             |

### 4. Command 개발 규칙

`.claude/commands/` 아래에 Markdown 파일로 작성:

```markdown
# Command: do-example

## 목적

이 커맨드의 목적을 설명합니다.

## 실행 조건

- 조건 1
- 조건 2

## 프롬프트

실제 Claude에게 전달될 지시사항을 작성합니다.
```

### 5. 테스트 방법

1. 이 프로젝트 디렉토리에서 Claude Code 실행
2. 개발 중인 hook/command가 적용됨
3. 정상 동작 확인 후 배포

```bash
# 테스트 후 배포
./scripts/deploy.sh
```

## 파일 구조 규칙

```
.claude/
├── hooks/
│   └── *.py          # Python 스크립트, 실행 권한 필요
├── commands/
│   └── *.md          # Markdown 형식
└── settings.json     # 개발용 설정
```

## 배포 전 체크리스트

- [ ] Hook 스크립트에 실행 권한 있음 (`chmod +x`)
- [ ] 경로가 `$CLAUDE_PROJECT_DIR` 사용
- [ ] stdin/stdout/stderr 올바르게 사용
- [ ] exit code 올바르게 반환
- [ ] 이 프로젝트에서 테스트 완료
