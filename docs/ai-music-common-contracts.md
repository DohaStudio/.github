# DohaStudio AI Music Common Contracts

> 상태: [제안]
> 마지막 검토일: 2026-08-11
> 기준 결정: [ADR-001](decisions/ADR-001-common-ai-music-contracts.md)

## 1. 목적

DohaLM, DohaMusic, DohaAudio와 DohaVocal이 같은 객체 이름을 다른 의미로 구현하지 않도록 Repository 간 공통 의미 계약을 정의합니다. 상세 field·enum·불변 조건은 [Specification Index](specifications/README.md)를 따릅니다.

## 2. 객체와 책임

| 객체 | 주 생성자 | 주요 소비자 | 핵심 책임 |
|---|---|---|---|
| MusicIntent | DohaLM/DohaMusic | DohaMusic, DohaAudio, DohaVocal | 실행 가능한 음악 작업 의도 |
| LearningCandidate | DohaMusic/검토 계층 | Dataset governance | 학습 검토 후보 |
| ReferenceAnalysis | DohaAudio/DohaVocal | DohaLM, DohaMusic | reference 분석 identity |
| FeatureRecord | DohaAudio/DohaVocal | DohaLM, Similarity | versioned 음악 feature |
| SimilarityReport | Similarity capability | DohaLM, DohaMusic | 창작 지원 유사도 위험 |
| RevisionPlan | DohaLM | DohaMusic, Providers | 승인 전 수정 계획 |
| DatasetVersion | Dataset governance | Training | frozen 학습 입력 |
| TrainingRun | Training owner | Evaluation | 단일 학습 실행 identity |
| EvaluationRun | Evaluation owner | Model approval | metric·human review 결과 |
| ModelVersion | Model governance | Provider Runtime | 승인 모델·adapter identity |
| ProviderCapability | 각 Provider | DohaMusic | 지원 기능과 schema |
| RightsMetadata | 권리 검토 계층 | 모든 Gate | 목적별 권리·consent |
| TrainingEligibility | Dataset governance | DatasetVersion | 학습 진입 fail-closed 판정 |

## 3. Repository 경계

- DohaMusic은 사용자 작업, Project/Asset state, 승인과 orchestration을 소유합니다.
- DohaLM은 planning, lyrics, prompt, QA, similarity 해석과 RevisionPlan을 소유합니다.
- DohaAudio는 audio/music generation, stem, audio analysis, similarity 계산과 mix 처리를 소유합니다.
- DohaVocal은 singing, voice conversion, vocal analysis와 vocal edit를 소유합니다.
- Provider끼리 직접 호출하지 않고 DohaMusic이 MusicIntent와 Capability를 이용해 orchestration합니다.

## 4. Reference와 학습 경계

```text
Reference Audio → ReferenceAnalysis → FeatureRecord → DohaLM Context
                                                   → Planning/Generation/Revision
```

Reference Audio는 직접 학습하지 않습니다. 학습 후보는 다음을 결합할 수 있습니다.

- 목적별 사용이 승인된 FeatureRecord
- 사용자가 만든 작업 결과
- 사용자 수정 결과
- 사용자 선택·preference

각 항목은 RightsMetadata와 TrainingEligibility를 통과해야 합니다.

## 5. Lineage

```text
LearningCandidate
  → TrainingEligibility
  → DatasetVersion
  → TrainingRun
  → EvaluationRun
  → ModelVersion
  → Provider Runtime
```

각 단계는 immutable ID와 parent reference를 보존합니다. 다음 단계의 생성은 이전 단계 상태를 소급 변경하지 않습니다.

## 6. 금지 사항

- Reference Audio의 Dataset 직접 포함 또는 자동 학습
- 사용자 승인·권리 검토 없는 작업 결과 수집
- SimilarityReport를 법적 판정으로 표시
- Evaluation 승인 없이 ModelVersion을 Runtime에 승격
- Repository 전용 의미를 공통 enum에 임의 추가
- 문서 상태 [제안]을 구현·배포 완료로 표현

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 객체 책임, Repository 경계, reference 학습 경계와 lineage 정의 |
