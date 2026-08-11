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
| LearningCandidate | DohaMusic | DohaLM Dataset governance | 학습 검토 후보와 발생 이력 |
| ReferenceAnalysis | DohaAudio/DohaVocal | DohaLM, DohaMusic | reference 분석 identity |
| FeatureRecord | DohaAudio/DohaVocal | DohaLM, Similarity | versioned 음악 feature |
| SimilarityReport | Similarity capability | DohaLM, DohaMusic | 창작 지원 유사도 위험 |
| RevisionPlan | DohaLM | DohaMusic, Providers | 승인 전 수정 계획 |
| DatasetVersion | DohaLM | Training | Dataset 논리 권위와 frozen 학습 입력 |
| TrainingRun | DohaLM | Evaluation | 단일 학습 실행 identity |
| EvaluationRun | DohaLM | Model approval | metric·human review와 approval evidence |
| ModelVersion | DohaLM | Provider Runtime | Model 논리 권위와 Runtime Gate |
| ProviderCapability | 각 Provider | DohaMusic | 지원 기능과 schema |
| RightsMetadata | 권리 검토 계층 | 모든 Gate | 목적별 권리·consent |
| TrainingEligibility | Dataset governance | DatasetVersion | 학습 진입 fail-closed 판정 |

## 3. Repository 경계

- DohaMusic은 사용자 작업·가사 원본·수정·선택, Rights/Provenance/Consent, LearningCandidate 발생 이력, Project/Asset/Job state와 orchestration을 소유합니다.
- DohaLM은 DatasetVersion·TrainingRun·EvaluationRun·ModelVersion, planning, lyrics, prompt, QA, similarity 해석과 RevisionPlan을 소유합니다.
- DohaAudio는 audio/music generation, stem, Feature 추출, similarity 계산과 mix 처리를 소유합니다.
- DohaVocal은 singing, voice conversion, vocal analysis와 vocal edit를 소유합니다.
- Provider끼리 직접 호출하지 않고 DohaMusic이 MusicIntent와 Capability를 이용해 orchestration합니다.

| 영역 | 권위 저장소 |
|---|---|
| 사용자 작업·가사 원본·수정·선택 | DohaMusic |
| Rights / Provenance / Consent | DohaMusic |
| LearningCandidate 발생 이력 | DohaMusic |
| DatasetVersion / TrainingRun / EvaluationRun / ModelVersion | DohaLM |
| 음원 Feature 추출·음악 Similarity 계산 | DohaAudio |
| Vocal-specific Feature·processing | DohaVocal |
| 분석 해석 / Song Planning / RevisionPlan | DohaLM |
| Workspace / Job / Artifact / Composition lineage | DohaMusic |
| 교차 저장소 객체 의미 계약 | DohaStudio/.github Common Specification |

Common Specification은 Runtime 데이터 소유권이나 각 저장소 내부 DB 권위를 가져가지 않습니다.

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
  → DatasetManifest
  → TrainingRun
  → EvaluationRun
  → ModelVersion
  → ModelManifest
  → Provider Runtime
```

각 단계는 immutable ID와 parent reference를 보존합니다. 다음 단계의 생성은 이전 단계 상태를 소급 변경하지 않습니다.

DatasetVersion과 ModelVersion은 논리적 source of truth이고, 각 Manifest는 Version을 재현하는 발행 후 immutable evidence입니다. Candidate TrainingEligibility 통과 뒤에도 Dataset 집합 eligibility·review·Manifest 발행·Freeze가 필요합니다. Runtime 승격은 완료·승인된 EvaluationRun과 ModelVersion의 복합 `runtime_allowed` invariant만 권위를 가집니다.

## 6. 금지 사항

- Reference Audio의 Dataset 직접 포함 또는 자동 학습
- 사용자 승인·권리 검토 없는 작업 결과 수집
- SimilarityReport를 법적 판정으로 표시
- Evaluation 승인 없이 ModelVersion을 Runtime에 승격
- Repository 전용 의미를 공통 enum에 임의 추가
- 문서 상태 [제안]을 구현·배포 완료로 표현

## 7. Security와 Privacy

공통 객체와 예제에는 credential, API key, access token, 개인 절대 경로, 실제 Dataset/weight 경로, 사용자 원문, 권리 문서 원문, signed URL, 내부 storage root, raw Provider error와 stack trace를 포함하지 않습니다. Reference feature와 embedding은 재식별·원본 추론 위험이 있으므로 원본과 별도의 storage·access·retention 권한을 적용합니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 객체 책임, Repository 경계, reference 학습 경계와 lineage 정의 |
