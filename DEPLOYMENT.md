# 배포 가이드

## 배포 프로세스

### 1. 배포 실행

```bash
./scripts/deploy.sh
```

**수행 작업:**

1. `.claude/hooks/` → `~/.claude/hooks/` 복사
2. `.claude/commands/` → `~/.claude/commands/` 복사
3. `settings.json` 병합 (기존 설정 유지 + commands/hooks 추가)
4. 경로 자동 변환 (`$CLAUDE_PROJECT_DIR` → `~/.claude`)
5. Git 커밋 생성

**출력 예시:**

```
=== Claude Hooks 배포 ===
Source: /home/user/git/claude/.claude/
Target: /home/user/.claude/

Source commit: abc1234 (main)
Source message: Add new hook

Copying files...
Merging settings.json...
  - commands, hooks 병합 완료 (경로 변환: $CLAUDE_PROJECT_DIR → ~/.claude)

Committing changes...
[main def5678] Deploy from main@abc1234: Add new hook

=== 배포 완료 ===
Deployed commit: def5678
```

### 2. 배포 확인

```bash
# 배포된 파일 확인
ls -la ~/.claude/hooks/
ls -la ~/.claude/commands/

# settings.json 확인
cat ~/.claude/settings.json

# 배포 히스토리 확인
./scripts/rollback.sh
```

## 롤백

### 배포 히스토리 조회

```bash
./scripts/rollback.sh
```

**출력 예시:**

```
=== 배포 히스토리 ===

def5678 2026-01-02 12:05 Deploy from main@abc1234: Add new hook
abc1234 2026-01-02 11:55 Deploy from main@xyz9999: Initial
feea5a9 2026-01-02 11:53 Initial commit

Usage:
  rollback.sh <commit>  # 특정 버전으로 롤백
  rollback.sh HEAD~1    # 직전 버전으로 롤백

현재 버전: def5678
```

### 롤백 실행

```bash
# 특정 커밋으로 롤백
./scripts/rollback.sh abc1234

# 직전 버전으로 롤백
./scripts/rollback.sh HEAD~1
```

**롤백 시 확인 프롬프트:**

```
=== 롤백 실행 ===
Current: def5678
Target:  abc1234

Target commit info:
  abc1234 2026-01-02 11:55 Deploy from main@xyz9999: Initial

롤백을 진행하시겠습니까? (y/N)
```

## 배포 구조

### 경로 변환

| 개발 환경                               | 운영 환경             |
| --------------------------------------- | --------------------- |
| `$CLAUDE_PROJECT_DIR/.claude/hooks/`    | `~/.claude/hooks/`    |
| `$CLAUDE_PROJECT_DIR/.claude/commands/` | `~/.claude/commands/` |

### settings.json 병합

**병합 대상 키:**

- `commands` - 전체 교체
- `hooks` - 전체 교체 (경로 변환 포함)

**유지되는 키:**

- `model`
- `mcpServers`
- 기타 사용자 설정

## 문제 해결

### ~/.claude가 git 저장소가 아님

```bash
cd ~/.claude
git init
git add .gitignore settings.json
git commit -m "Initial commit"
```

### jq가 설치되어 있지 않음

```bash
# Ubuntu/Debian
sudo apt install jq

# macOS
brew install jq
```

### 배포 후 hook이 동작하지 않음

1. 실행 권한 확인:

   ```bash
   chmod +x ~/.claude/hooks/*.py
   ```

2. 경로 확인:

   ```bash
   cat ~/.claude/settings.json | jq '.hooks'
   ```

3. Python 경로 확인:
   ```bash
   which python3
   ```
