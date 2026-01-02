#!/bin/bash
set -e

TARGET_DIR="$HOME/.claude"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ~/.claude가 git 저장소인지 확인
if [ ! -d "$TARGET_DIR/.git" ]; then
    echo -e "${RED}Error: $TARGET_DIR is not a git repository${NC}"
    exit 1
fi

cd "$TARGET_DIR"

# 인자가 없으면 배포 히스토리 출력
if [ -z "$1" ]; then
    echo -e "${GREEN}=== 배포 히스토리 ===${NC}"
    echo ""
    git log --oneline -20 --format="%C(yellow)%h%C(reset) %C(cyan)%cd%C(reset) %s" --date=format:"%Y-%m-%d %H:%M"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  rollback.sh <commit>  # 특정 버전으로 롤백"
    echo "  rollback.sh HEAD~1    # 직전 버전으로 롤백"
    echo ""
    echo -e "${YELLOW}현재 버전:${NC} $(git rev-parse --short HEAD)"
    exit 0
fi

TARGET_COMMIT="$1"

# 대상 커밋 존재 확인
if ! git rev-parse "$TARGET_COMMIT" >/dev/null 2>&1; then
    echo -e "${RED}Error: Commit '$TARGET_COMMIT' not found${NC}"
    exit 1
fi

# 현재 상태 저장
CURRENT_COMMIT=$(git rev-parse --short HEAD)
TARGET_SHORT=$(git rev-parse --short "$TARGET_COMMIT")

echo -e "${GREEN}=== 롤백 실행 ===${NC}"
echo -e "Current: ${RED}$CURRENT_COMMIT${NC}"
echo -e "Target:  ${GREEN}$TARGET_SHORT${NC}"
echo ""

# 대상 커밋 정보 출력
echo -e "${YELLOW}Target commit info:${NC}"
git log -1 --format="  %h %cd %s" --date=format:"%Y-%m-%d %H:%M" "$TARGET_COMMIT"
echo ""

# 확인
read -p "롤백을 진행하시겠습니까? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "롤백이 취소되었습니다."
    exit 0
fi

# hooks와 commands만 롤백 (다른 파일은 건드리지 않음)
echo ""
echo -e "${GREEN}Restoring hooks and commands...${NC}"

# 대상 커밋에서 hooks와 commands 복원
git checkout "$TARGET_COMMIT" -- hooks/ commands/ 2>/dev/null || {
    echo -e "${YELLOW}Warning: Some files may not exist in target commit${NC}"
    git checkout "$TARGET_COMMIT" -- hooks/ 2>/dev/null || true
    git checkout "$TARGET_COMMIT" -- commands/ 2>/dev/null || true
}

# 롤백 커밋 생성
git add hooks/ commands/
ROLLBACK_MSG="Rollback to $TARGET_SHORT (from $CURRENT_COMMIT)"
git commit -m "$ROLLBACK_MSG" --allow-empty

FINAL_COMMIT=$(git rev-parse --short HEAD)
echo ""
echo -e "${GREEN}=== 롤백 완료 ===${NC}"
echo -e "New commit: ${GREEN}$FINAL_COMMIT${NC}"
echo ""
echo -e "${YELLOW}Note:${NC} 롤백을 취소하려면 다음 명령어를 실행하세요:"
echo "  ./scripts/rollback.sh $CURRENT_COMMIT"
