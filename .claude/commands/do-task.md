---
description: 기능의 다음 작업을 자동으로 식별하고 실행, 완료 시 체크리스트 리뷰
allowed-tools: ["Bash", "Write", "Read", "Edit", "Ls"]
model: claude-3-5-sonnet-20241022
argument-hint: <feature-name>
---

# Auto-Resume Task Execution Protocol

**Target**: `TODO/$1` 디렉토리의 잔여 작업을 자동으로 식별하고 실행합니다.

## 1. Context Loading (State Check)

작업 수행을 위해 다음 문맥을 로드합니다:

- **Project Rules**: `@CLAUDE.md` (코딩 컨벤션)
- **Feature Plan**: `@TODO/$1/PLAN.md` (전체 계획)
- **Progress Log**: `@TODO/$1/progress.md` (현재 진행 상태)

## 2. Next Task Identification (Reasoning)

**스스로 판단하여 다음 작업을 결정하십시오:**

1. `ls TODO/$1` 명령을 실행하여 해당 폴더 내의 파일 목록을 확인
2. `progress.md`의 기록을 분석하여 이미 완료된 작업(`Completed` 또는 `✅`)을 파악
3. 숫자 순서상 **그 다음으로 진행해야 할 작업 파일**을 찾음
   - 예시: `01.md`가 완료되었다면 `02.md`를 읽고 실행

## 3. Task Execution (Implementation)

**작업 파일이 남아있는 경우:**

1. 해당 작업 파일(예: `02.md`)을 `Read` 도구로 읽음
2. 작업 파일의 지시사항에 따라 코드를 작성하거나 수정
3. 코드 수정 후 `CLAUDE.md`에 정의된 테스트/린트 실행하여 검증
4. `progress.md`에 결과 기록:
   ```markdown
   - [{현재 날짜/시간}] 02.md Completed: {간략한 구현 내용}
   ```
5. progress.md의 작업 현황 테이블 업데이트:
   ```markdown
   | 02.md | ✅ 완료 | {현재 시간} |
   ```

## 4. All Tasks Completed Check

**모든 작업 파일이 완료된 경우:**

다음 순서로 **체크리스트 리뷰**를 수행하십시오:

### 4.1 체크리스트 로드

```
@TODO/$1/checklist.md
```

### 4.2 각 항목 검증

체크리스트의 각 항목을 확인하고 검증합니다:

**코드 품질 항목:**

```bash
# 린트 검사
npm run lint

# 테스트 실행
npm run test

# 타입 검사 (있는 경우)
npm run typecheck
```

**기능 요구사항 항목:**

- 구현된 코드를 검토하여 요구사항 충족 여부 확인
- 미충족 항목이 있으면 해당 부분 수정

### 4.3 체크리스트 업데이트

검증 통과한 항목은 체크 표시로 업데이트:

```markdown
- [x] 린트 통과 (npm run lint)
- [x] 테스트 통과 (npm run test)
```

### 4.4 미완료 항목 처리

미완료 항목이 있는 경우:

1. 해당 항목을 해결하기 위한 작업 수행
2. 다시 검증
3. 모든 항목이 완료될 때까지 반복

### 4.5 리뷰 완료 보고

모든 체크리스트 항목이 완료되면:

```
🎉 모든 작업 및 체크리스트 리뷰가 완료되었습니다!

📊 최종 결과:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 작업 파일: {N}개 완료
✅ 체크리스트: {M}개 항목 모두 통과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 단계:
  /do-commit $1   - 변경사항 커밋
  /do-deploy      - 배포 실행
```

## 5. Progress Update

progress.md의 상태를 업데이트:

**작업 진행 중:**

```markdown
## 현재 상태: 🔵 작업 진행 중 (N/M 완료)
```

**모든 작업 완료 + 체크리스트 통과:**

```markdown
## 현재 상태: ✅ 구현 완료

### 완료율

- 체크리스트: {M}/{M} (100%)
```

## 6. Report (작업 진행 중인 경우)

```
✅ 작업 완료: {task_name}

수행 내용:
  - {변경 사항 1}
  - {변경 사항 2}

남은 작업: {remaining_count}개
  - {next_task_name}
  - ...

다음 단계:
  /do-task $1       - 다음 작업 실행
  /do-progress $1   - 진행 상황 확인
```
