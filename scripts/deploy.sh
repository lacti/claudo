#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$HOME/.claude"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Claude Hooks 배포 ===${NC}"
echo "Source: $PROJECT_DIR/.claude/"
echo "Target: $TARGET_DIR/"
echo ""

# 소스 프로젝트의 git 정보 가져오기
cd "$PROJECT_DIR"
SOURCE_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
SOURCE_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
SOURCE_MSG=$(git log -1 --format="%s" 2>/dev/null || echo "unknown")

echo -e "${YELLOW}Source commit:${NC} $SOURCE_COMMIT ($SOURCE_BRANCH)"
echo -e "${YELLOW}Source message:${NC} $SOURCE_MSG"
echo ""

# ~/.claude가 git 저장소인지 확인
if [ ! -d "$TARGET_DIR/.git" ]; then
    echo -e "${RED}Error: $TARGET_DIR is not a git repository${NC}"
    echo "Initialize with: cd ~/.claude && git init"
    exit 1
fi

# 배포 전 상태 확인
cd "$TARGET_DIR"
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Warning: Uncommitted changes in $TARGET_DIR${NC}"
    git status --short
    echo ""
fi

# 파일 복사
echo -e "${GREEN}Copying files...${NC}"
cp -r "$PROJECT_DIR/.claude/hooks" "$TARGET_DIR/"
cp -r "$PROJECT_DIR/.claude/commands" "$TARGET_DIR/"

# settings.json 병합 (기존 설정 유지 + 프로젝트의 commands/hooks만 추가)
echo -e "${GREEN}Merging settings.json...${NC}"
SOURCE_SETTINGS="$PROJECT_DIR/.claude/settings.json"
TARGET_SETTINGS="$TARGET_DIR/settings.json"

if [ -f "$SOURCE_SETTINGS" ] && [ -f "$TARGET_SETTINGS" ]; then
    # 프로젝트에서 commands와 hooks만 추출하여 기존 설정에 병합
    # hooks 경로 변환: $CLAUDE_PROJECT_DIR/.claude/ → ~/.claude/
    # jq: 기존 설정 + 프로젝트의 commands/hooks (프로젝트 값이 우선)
    MERGED=$(jq -s '
        .[0] as $target |
        .[1] as $source |

        # hooks 경로 변환 함수
        def transform_hooks:
            if . then
                walk(
                    if type == "string" then
                        gsub("\"\\$CLAUDE_PROJECT_DIR\"/.claude/"; "~/.claude/") |
                        gsub("\\$CLAUDE_PROJECT_DIR/.claude/"; "~/.claude/")
                    else .
                    end
                )
            else null
            end;

        # commands 경로 변환 (file 필드)
        def transform_commands:
            if . then
                map(
                    if .file then
                        .file |= (
                            gsub("\"\\$CLAUDE_PROJECT_DIR\"/.claude/"; "~/.claude/") |
                            gsub("\\$CLAUDE_PROJECT_DIR/.claude/"; "~/.claude/")
                        )
                    else .
                    end
                )
            else null
            end;

        $target * {
            commands: (($source.commands | transform_commands) // $target.commands),
            hooks: (($source.hooks | transform_hooks) // $target.hooks)
        }
    ' "$TARGET_SETTINGS" "$SOURCE_SETTINGS")

    echo "$MERGED" > "$TARGET_SETTINGS"
    echo "  - commands, hooks 병합 완료 (경로 변환: \$CLAUDE_PROJECT_DIR → ~/.claude)"
elif [ -f "$SOURCE_SETTINGS" ] && [ ! -f "$TARGET_SETTINGS" ]; then
    # 대상에 settings.json이 없으면 복사
    cp "$SOURCE_SETTINGS" "$TARGET_SETTINGS"
    echo "  - settings.json 복사 완료"
fi

# 변경사항 확인
cd "$TARGET_DIR"
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}No changes to deploy${NC}"
    exit 0
fi

# Git 커밋
echo ""
echo -e "${GREEN}Committing changes...${NC}"
git add hooks/ commands/ settings.json
DEPLOY_MSG="Deploy from $SOURCE_BRANCH@$SOURCE_COMMIT: $SOURCE_MSG"
git commit -m "$DEPLOY_MSG"

# 결과 출력
DEPLOY_COMMIT=$(git rev-parse --short HEAD)
echo ""
echo -e "${GREEN}=== 배포 완료 ===${NC}"
echo -e "Deployed commit: ${GREEN}$DEPLOY_COMMIT${NC}"
echo ""
echo -e "${YELLOW}롤백 방법:${NC}"
echo "  ./scripts/rollback.sh          # 최근 배포 목록 보기"
echo "  ./scripts/rollback.sh <commit> # 특정 버전으로 롤백"
