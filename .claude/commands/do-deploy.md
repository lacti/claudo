---
description: 배포 지시 파일(DEPLOY.md)을 읽고 배포 프로세스를 실행
allowed-tools: ["Bash", "Read", "Write"]
model: claude-3-5-sonnet-20241022
argument-hint: [environment] [--init]
---

# Deployment Protocol

**목표**: 프로젝트의 배포 지시 파일을 확인하고, 정의된 프로세스에 따라 배포를 실행합니다.

## Input Parsing

- `$1` (선택): 배포 환경 지정 (production, staging, dev 등)
- `--init`: DEPLOY.md 템플릿 생성
- 환경 미지정 시 DEPLOY.md의 기본 환경 사용

## Execution Steps

### 1. 배포 지시 파일 확인

다음 순서로 배포 지시 파일을 검색하십시오:

```
1. ./DEPLOY.md (프로젝트 루트)
2. ./deploy/DEPLOY.md
3. ./docs/DEPLOY.md
4. ./.claude/DEPLOY.md
```

### 2. 파일이 존재하지 않는 경우

**즉시 중단**하고 다음 메시지를 출력하십시오:

```
⚠️  배포 지시 파일을 찾을 수 없습니다.

배포를 실행하려면 DEPLOY.md 파일이 필요합니다.
다음 위치 중 하나에 파일을 생성해주세요:

  📄 ./DEPLOY.md (권장)
  📄 ./deploy/DEPLOY.md
  📄 ./.claude/DEPLOY.md

DEPLOY.md 템플릿을 생성하시겠습니까?
  /do-deploy --init
```

### 3. --init 옵션이 있는 경우

DEPLOY.md 템플릿을 생성하십시오:

```markdown
# 배포 가이드

## 환경 설정

### Production
- **URL**: https://example.com
- **브랜치**: main
- **자동 배포**: false

### Staging
- **URL**: https://staging.example.com
- **브랜치**: develop
- **자동 배포**: true

## 사전 조건 (Pre-requisites)

배포 전 다음 항목을 확인하세요:
- [ ] 모든 테스트 통과 (`npm run test`)
- [ ] 린트 검사 통과 (`npm run lint`)
- [ ] 빌드 성공 (`npm run build`)
- [ ] 환경 변수 설정 완료

## 배포 절차

### 1. 빌드
\`\`\`bash
npm run build
\`\`\`

### 2. 테스트
\`\`\`bash
npm run test
\`\`\`

### 3. 배포 실행
\`\`\`bash
# Production
npm run deploy:prod

# Staging
npm run deploy:staging
\`\`\`

## 롤백 절차

문제 발생 시:
\`\`\`bash
# 이전 버전으로 롤백
npm run rollback
\`\`\`

## 배포 후 확인

- [ ] 헬스체크 엔드포인트 확인
- [ ] 주요 기능 수동 테스트
- [ ] 에러 로그 모니터링
```

### 4. 파일이 존재하는 경우

DEPLOY.md 파일을 읽고 다음을 수행하십시오:

#### 4.1 환경 확인
```
🚀 배포 준비

환경: {environment}
브랜치: {current_branch}
최신 커밋: {commit_hash} - {commit_message}

배포 대상: {target_url}
```

#### 4.2 사전 조건 검사

DEPLOY.md의 "사전 조건" 섹션에 정의된 명령어들을 순차적으로 실행:

```bash
# 예시
npm run test
npm run lint
npm run build
```

**하나라도 실패하면 즉시 중단:**
```
❌ 사전 조건 검사 실패

실패한 단계: {step_name}
오류 메시지: {error_message}

배포가 중단되었습니다. 위 오류를 해결한 후 다시 시도하세요.
```

#### 4.3 배포 실행

DEPLOY.md의 "배포 절차" 섹션에 정의된 명령어를 실행:

```
📦 배포 진행 중...

[1/3] 빌드 중... ✅
[2/3] 테스트 실행 중... ✅
[3/3] 배포 중... ✅
```

#### 4.4 배포 후 확인

DEPLOY.md의 "배포 후 확인" 섹션의 체크리스트를 표시:

```
✅ 배포 완료!

배포 후 확인사항:
- [ ] 헬스체크 엔드포인트 확인
- [ ] 주요 기능 수동 테스트
- [ ] 에러 로그 모니터링

배포 정보:
  환경: {environment}
  시간: {timestamp}
  커밋: {commit_hash}
  버전: {version}
```

### 5. 배포 기록

배포 성공 시, 활성화된 TODO 디렉토리의 progress.md에 기록:

```markdown
- [{현재 날짜/시간}] 🚀 Deployed to {environment}: {commit_hash}
```

## Safety Rules

- **Production 배포 전 반드시 확인 프롬프트 표시**
- **main/master 브랜치가 아닌 경우 경고**
- **uncommitted changes가 있으면 배포 차단**
- **DEPLOY.md에 정의되지 않은 명령어는 실행하지 않음**
