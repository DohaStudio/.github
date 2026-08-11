# ADR-001: AI Music Common Contracts 도입

- 상태: `draft`
- 결정일: 미결정
- 마지막 검토일: 2026-08-11

## 배경

DohaLM, DohaMusic, DohaAudio와 DohaVocal은 음악 의도, 분석 feature, 학습 candidate, Dataset/Model lineage와 권리 상태를 교환해야 합니다. Repository별로 비슷한 이름을 독립 정의하면 의미·상태·승인 경계가 달라지고 Reference Audio의 부적절한 학습, 권리 상태 혼합과 Runtime 오승격 위험이 생깁니다.

## 제안 결정

1. [Specification Index](../specifications/README.md)의 13개 객체를 조직 공통 의미 계약으로 사용합니다.
2. 모든 객체는 versioned schema, immutable identity, 명시적 lineage와 fail-closed 검증을 사용합니다.
3. DohaMusic이 Provider orchestration과 사용자 승인을 소유하고 Provider끼리 직접 호출하지 않습니다.
4. Reference Audio는 직접 학습하지 않고 승인된 FeatureRecord와 사용자 작업·수정·선택만 candidate가 될 수 있습니다.
5. SimilarityReport는 창작 지원 분석이며 법적 판정이 아닙니다.
6. candidate approval, training eligibility, evaluation approval과 runtime eligibility를 독립 Gate로 둡니다.
7. 교차 저장소 계약은 이 Common Specification이 소유하지만 Runtime 데이터는 각 저장소가 소유합니다. DohaMusic은 사용자 작업·Rights/Provenance/Consent·LearningCandidate·Workspace lineage를, DohaLM은 DatasetVersion·TrainingRun·EvaluationRun·ModelVersion과 Planning/RevisionPlan을, DohaAudio는 Feature·Similarity 계산을 소유합니다.
8. DatasetVersion과 ModelVersion을 논리적 source of truth로, DatasetManifest와 ModelManifest를 ID·checksum으로 결속된 발행 후 immutable 재현 evidence로 사용합니다. Manifest는 Version의 approval·lifecycle을 독립 변경할 수 없습니다.
9. TrainingEligibility는 Candidate 단위 학습 Gate로 제한합니다. Dataset 집합 Gate는 DatasetVersion이, Runtime 승격은 완료·승인 EvaluationRun과 ModelVersion의 복합 `runtime_allowed` invariant가 소유합니다.
10. lineage는 LearningCandidate → TrainingEligibility → DatasetVersion → DatasetManifest → TrainingRun → EvaluationRun → ModelVersion → ModelManifest → Provider Runtime을 보존합니다.

## 영향

### 장점

- Repository 간 객체 의미와 version compatibility를 고정합니다.
- 권리·학습·Runtime 승격을 audit 가능한 lineage로 연결합니다.
- Reference와 similarity의 제품·법률 경계를 명확히 합니다.

### 비용과 위험

- 각 Repository에 mapping과 compatibility validation이 필요합니다.
- 기존 기준선과 field naming의 Repository별 compatibility mapping이 필요합니다.
- 권리·similarity threshold는 정책·법무 검토 없이는 확정할 수 없습니다.

## 검토한 대안

1. Repository별 독립 schema: 초기 속도는 빠르지만 동일 용어의 의미와 version이 분기되어 기각합니다.
2. DohaMusic 내부 단일 schema: orchestration에는 단순하지만 Provider의 모델·권리·학습 lineage를 충분히 표현하지 못해 기각합니다.
3. 구현을 먼저 만들고 문서를 추출: 호환성 파괴와 권리 Gate 누락 위험이 커서 기각합니다.

## Migration

승인 후 `ORG-02: Common AI Contract Schema v1`에서 Common Envelope, MusicIntent, ProviderCapability, RightsMetadata와 TrainingEligibility JSON Schema, version policy, compatibility validator와 synthetic valid/invalid fixture를 만듭니다. 각 Repository는 기존 객체와 mapping을 문서화하고 compatibility layer로 전환합니다.

기존 DohaLM REST/SSE와 Adapter Loader는 즉시 재구성하지 않고 Compatibility Layer 뒤에 보존합니다. Directory Reorganization보다 mapping layer를 먼저 수행해야 기존 API·artifact identity·rollback 경계를 동시에 바꾸는 위험을 피할 수 있습니다. 기존 Version·Manifest·Run을 제자리 변경하지 않고 새 version 또는 `supersedes` replacement를 사용합니다.

## 재검토 조건

- 공통 계약이 Provider 구현을 표현하지 못할 때
- 권리·privacy·법무 검토가 현재 field로 표현되지 않을 때
- Repository 간 version negotiation이 실패할 때
- Version/Manifest 권위 또는 immutable replacement 계약이 운영 오류를 만들 때

## 제외

이번 결정은 Provider Runtime, Training, Inference, Dataset, REST, Streaming, Worker, Job, DB 또는 실제 code 구현을 승인하지 않습니다.

## 승인 전 상태

ADR 승인 전 모든 Specification은 `[제안]`이며 production compatibility를 보장하지 않습니다. 승인 후에도 Repository별 구현은 별도 PR입니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 공통 객체·권리·lineage·Provider 책임 결정 초안 작성 |
