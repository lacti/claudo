# Claude Code Extensions

Claude Code의 Hooks와 Commands를 개발하고 관리하기 위한 프로젝트입니다.

## 구성 요소

### Hooks

| Hook              | 트리거           | 설명                                          |
| ----------------- | ---------------- | --------------------------------------------- |
| `gatekeeper.py`   | UserPromptSubmit | 복잡한 작업 감지 시 `/plan-feature` 사용 권장 |
| `auto_logger.py`  | PostToolUse      | 도구 사용 후 자동 로깅                        |
| `quality_gate.py` | Stop             | 작업 완료 시 품질 검증                        |

### Commands

| Command        | 설명                                             |
| -------------- | ------------------------------------------------ |
| `/do-plan`     | 기능 구현을 위한 계획 수립 및 작업 파일 생성     |
| `/do-todo`     | Plan mode 검토 완료된 계획을 TODO 파일로 변환    |
| `/do-task`     | 다음 작업을 자동으로 식별하고 실행               |
| `/do-commit`   | 변경점을 분석하여 git commit 생성                |
| `/do-progress` | checklist.md 기반 진행률 표시                    |
| `/do-deploy`   | DEPLOY.md를 읽고 배포 프로세스 실행              |

## 빠른 시작

```bash
# 1. 저장소 클론
git clone <repository-url>
cd claude

# 2. 설치 (최초 1회)
./scripts/deploy.sh

# 3. MCP 서버 추가 (선택)
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

## 문서

- [INSTALL.md](./INSTALL.md) - 설치 방법
- [DEPLOYMENT.md](./DEPLOYMENT.md) - 배포 가이드
- [CLAUDE.md](./CLAUDE.md) - 개발 가이드

## 디렉토리 구조

```
claude/
├── .claude/
│   ├── hooks/           # Hook 스크립트
│   ├── commands/        # Command 정의
│   └── settings.json    # 개발용 설정
├── scripts/
│   ├── deploy.sh        # 배포 스크립트
│   └── rollback.sh      # 롤백 스크립트
├── README.md
├── INSTALL.md
├── DEPLOYMENT.md
└── CLAUDE.md
```

## 워크플로우

```
[개발] .claude/ 내 hooks, commands 수정
   ↓
[테스트] 이 프로젝트에서 Claude Code 실행
   ↓
[배포] ./scripts/deploy.sh
   ↓
[운영] 모든 프로젝트에서 ~/.claude/ 사용
```

## 라이선스

Private
