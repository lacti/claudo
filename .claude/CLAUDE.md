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
