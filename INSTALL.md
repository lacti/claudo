# 설치 가이드

## 사전 요구사항

- Claude Code CLI 설치됨
- Python 3.x
- jq (JSON 처리용)
- Git

### jq 설치

```bash
# Ubuntu/Debian
sudo apt install jq

# macOS
brew install jq

# 확인
jq --version
```

## 설치 단계

### 1. 저장소 클론

```bash
git clone <repository-url> ~/git/claude
cd ~/git/claude
```

### 2. ~/.claude Git 저장소 초기화

```bash
# ~/.claude 디렉토리로 이동
cd ~/.claude

# Git 저장소 초기화
git init

# .gitignore 생성
cat > .gitignore << 'EOF'
# 모든 것 제외
*

# 관리 대상 포함
!.gitignore
!settings.json
!hooks/
!hooks/**
!commands/
!commands/**

# 민감 정보 제외
.credentials.json
EOF

# 초기 커밋
git add .gitignore settings.json
git commit -m "Initial commit: settings.json and .gitignore"
```

### 3. 배포 실행

```bash
cd ~/git/claude
./scripts/deploy.sh
```

### 4. 설치 확인

```bash
# 배포된 파일 확인
ls ~/.claude/hooks/
ls ~/.claude/commands/

# Claude Code에서 명령어 확인
claude
# 프롬프트에서 /do- 입력 시 자동완성 확인
```

## 선택적 설정

### Chrome DevTools MCP 서버 추가

```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

### 모델 설정

`~/.claude/settings.json`에서 직접 수정:

```json
{
  "model": "opus"
}
```

## 업데이트

저장소에서 최신 변경사항을 가져온 후 재배포:

```bash
cd ~/git/claude
git pull
./scripts/deploy.sh
```

## 제거

### Hooks/Commands만 제거

```bash
rm -rf ~/.claude/hooks
rm -rf ~/.claude/commands
```

### settings.json에서 설정 제거

`~/.claude/settings.json`에서 `commands`와 `hooks` 키 삭제

## 문제 해결

### "~/.claude is not a git repository" 오류

```bash
cd ~/.claude
git init
git add .gitignore settings.json
git commit -m "Initial commit"
```

### Hook 실행 권한 오류

```bash
chmod +x ~/.claude/hooks/*.py
```

### Claude Code에서 명령어가 보이지 않음

1. Claude Code 재시작
2. settings.json 확인:
   ```bash
   cat ~/.claude/settings.json | jq '.commands'
   ```

### Python을 찾을 수 없음

시스템에 Python 3 설치 확인:

```bash
which python3
python3 --version
```
