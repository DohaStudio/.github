# AI Music Common Contracts Roadmap

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 현재 단계

이번 PR은 문서 계약만 작성합니다. 실제 schema와 Repository별 구현은 시작하지 않습니다.

## 후속 단계

| 단계 | 범위 | 완료 기준 |
|---|---|---|
| 1. Contract Review | 13개 객체·ADR 검토 | 용어·권리·책임 경계 승인 |
| 2. Schema Package | JSON Schema와 호환성 fixture | positive/negative validation 통과 |
| 3. Repository Mapping | DohaLM/Music/Audio/Vocal 내부 모델 mapping | 공통 의미를 보존한 adapter 설계 |
| 4. Capability Discovery | ProviderCapability 조회 계약 | 지원 version·상태 일치 |
| 5. Learning Governance | Candidate·Rights·Eligibility registry | 자동 승인 없는 audit trail |
| 6. Reference/Similarity | FeatureRecord·metric calibration | 원본 분리·비법률 경계 검증 |
| 7. Model Promotion | Run·Evaluation·ModelVersion 연결 | rollback 가능한 Runtime Gate |

각 단계는 별도 PR과 승인이 필요합니다. Runtime, Training, Dataset 처리, API, Worker, Job과 DB는 문서 승인만으로 자동 착수하지 않습니다.

## 권장 다음 PR

PR #5가 검토·병합된 뒤 `ORG-02: Common AI Contract Schema v1`을 권장합니다. Common Envelope, MusicIntent, ProviderCapability, RightsMetadata, TrainingEligibility의 JSON Schema, schema version policy, compatibility validator와 synthetic valid/invalid fixture만 포함합니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 문서 승인부터 schema·mapping·governance·promotion까지 단계 정의 |
