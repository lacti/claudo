---
description: Plan mode 검토 완료된 계획을 TODO 작업 파일로 변환
allowed-tools: ["Bash", "Write", "Read", "Glob"]
model: claude-3-5-sonnet-20241022
argument-hint: <task-name>
---

# Plan to TODO Conversion Protocol

**목표**: Claude Code plan mode에서 검토 완료된 계획을 `TODO/<task>/` 구조로 변환합니다.

## Input Parsing

`$1` = 작업명 (task_name)

- 띄어쓰기 대신 **하이픈(-)**을 사용하세요
- 예: `auth-system`, `deploy-pipeline`, `hook-refactor`

## Step 1: Plan 파일 탐지

`~/.claude/plans/` 디렉토리에서 **가장 최근 수정된** `.md` 파일을 찾습니다:

```bash
PLAN_FILE=$(ls -t ~/.claude/plans/*.md 2>/dev/null | head -1)
```

**파일을 찾을 수 없는 경우**:

```
❌ Plan 파일을 찾을 수 없습니다.

먼저 plan mode에서 계획을 수립하세요:
1. Claude Code에서 plan mode 진입
2. 계획 수립 및 검토 완료
3. /do-todo <task-name> 실행
```

## Step 2: Plan 파일 읽기 및 분석

Plan 파일을 읽고 다음 요소를 추출합니다:

- **제목**: 첫 번째 `#` 헤딩
- **개요**: 제목 다음 단락
- **단계들**: `### Step N:` 또는 `### Phase N:` 패턴
- **수정 대상 파일**: 파일 경로 패턴 (`path/to/file`)

## Step 3: Scaffolding

```bash
mkdir -p TODO/$1
```

## Step 4: Artifact Generation

다음 파일들을 **모두 반드시** 생성하십시오:

### A. TODO/$1/PLAN.md

Plan 파일의 내용을 기반으로 구조화:

```markdown
# $1 구현 계획

## 개요

{plan 파일의 개요 섹션}

## 목표

- [ ] {plan에서 도출한 목표 1}
- [ ] {plan에서 도출한 목표 2}

## 구현 단계

### Phase 1: {단계명}

- 작업 파일: 01.md
- 내용 요약

### Phase 2: {단계명}

- 작업 파일: 02.md
- 내용 요약

## 영향받는 파일

- `path/to/file` - 변경 사유

## 원본 Plan 파일

- 경로: {PLAN_FILE 경로}
- 수정일: {파일 수정 시간}
```

### B. TODO/$1/checklist.md

Plan의 각 단계에서 체크리스트 항목을 도출:

```markdown
# $1 품질 체크리스트

## 구현 요구사항

- [ ] {Step 1의 핵심 완료 조건}
- [ ] {Step 2의 핵심 완료 조건}
- [ ] ...

## 코드 품질

- [ ] 린트 통과
- [ ] 테스트 통과
- [ ] 타입 검사 통과

## 검증

- [ ] 수동 테스트 완료
- [ ] 엣지 케이스 처리 확인
```

### C. TODO/$1/progress.md

```markdown
# $1 진행 상황

## 현재 상태: 🟡 계획 수립 완료

### 타임라인

- [{현재 날짜/시간}] Plan converted from: {PLAN_FILE 이름}

### 작업 현황

| 작업  | 상태    | 완료 시간 |
| ----- | ------- | --------- |
| 01.md | ⏳ 대기 | -         |
| 02.md | ⏳ 대기 | -         |
| ...   | ...     | ...       |

### 완료율

- 체크리스트: 0/{총 항목 수} (0%)
```

### D. TODO/$1/01.md, 02.md, ... (세부 작업 파일)

Plan의 각 Step/Phase를 별도의 작업 파일로 변환:

```markdown
# 작업 01: {Step 제목}

## 목표

{Step의 설명에서 추출}

## 상세 지시사항

1. {Step 내용에서 추출한 구체적 작업}
2. ...

## 예상 변경 파일

- `path/to/file` - {변경 내용}

## 완료 기준

- [ ] {이 작업의 완료 조건}

## 참고사항

- 원본: {PLAN_FILE}의 Step N
```

## Step 5: Conclusion

```
✅ Plan이 TODO 구조로 변환되었습니다.

📁 TODO/$1/
├── PLAN.md         - 구현 계획
├── checklist.md    - 품질 체크리스트 ({N}개 항목)
├── progress.md     - 진행 상황
├── 01.md           - {작업 1 제목}
├── 02.md           - {작업 2 제목}
└── ...

원본 Plan: {PLAN_FILE}

다음 명령어:
  /do-task $1       - 작업 시작
  /do-progress $1   - 진행 상황 확인
```
