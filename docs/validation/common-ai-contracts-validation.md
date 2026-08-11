# AI Music Common Contracts 문서 정합성 검토

> 상태: [검토]
> 마지막 검토일: 2026-08-11
> 비교 기준: `develop`, 미병합 `docs/bootstrap-organization`, `docs/specifications`

## 1. 기준 상태

- `develop`에는 영문 root README만 존재했습니다.
- `docs/bootstrap-organization`에는 Ecosystem, Repository boundary, Roadmap와 ADR policy 제안이 있습니다.
- `docs/specifications`에는 Asset, AssetVersion, Artifact, Provider, Job, Model/Dataset Manifest, Composition Snapshot, Storage와 공통 용어 제안이 있습니다.
- 두 문서 브랜치는 이번 PR의 base가 아니므로 cherry-pick하거나 파일을 복사하지 않았습니다.

## 2. 용어 정합성

| 새 객체 | 기존 미병합 용어 | 판정 | 통합 규칙 |
|---|---|---|---|
| MusicIntent | AssetVersion, Composition Snapshot, Provider Capability | compatible | target은 정확한 AssetVersion을 참조 |
| ProviderCapability | Provider Contract의 `Capability` | compatible_extension | discovery 객체로 역할 구체화 |
| DatasetVersion | Dataset Manifest | overlap | DatasetVersion은 논리 lifecycle 객체, Manifest는 직렬화 evidence로 정리 필요 |
| ModelVersion | Model Manifest | overlap | ModelVersion은 논리 identity, Manifest는 artifact/evidence view로 정리 필요 |
| FeatureRecord | Artifact | compatible | FeatureRecord 직렬화본은 Artifact가 될 수 있으나 객체와 파일 ID를 분리 |
| LearningCandidate | Approval, Training Dataset | compatible_extension | 사용자 선택과 학습 승인을 분리 |
| ReferenceAnalysis | Recording, Enrollment, Training Dataset | compatible | Reference 원본과 Training Dataset 자동 동일시 금지 유지 |
| SimilarityReport | 기존 객체 없음 | new | 법적 판정이 아닌 창작 지원 객체 |

## 3. README·Roadmap·Specification·ADR 검토

| 대상 | 결과 |
|---|---|
| README | 새 문서 링크·비구현 범위·핵심 안전 경계 반영 |
| Roadmap | 문서 승인과 실제 구현 단계를 분리 |
| Specification | 공통 envelope와 13개 객체의 field·enum·불변 조건 작성 |
| ADR | draft 상태, 구현 비승인, 영향·대안·migration·재검토 경계 작성 |
| Architecture | DohaMusic orchestration과 Provider 비직접 호출 원칙 유지 |
| Lineage | Candidate→Dataset→Training→Evaluation→Model→Runtime 단방향 추적 정의 |

## 4. BLOCKER

1. `docs/bootstrap-organization`과 `docs/specifications`가 `develop`에 아직 병합되지 않아 후속 merge 순서에 따라 README·docs tree 충돌이 발생할 수 있습니다.
2. DatasetVersion/ModelVersion과 기존 Dataset/Model Manifest의 canonical source-of-truth 관계가 아직 승인되지 않았습니다.
3. 공통 schema package·compatibility test와 Repository별 mapping이 없으므로 production contract로 사용할 수 없습니다.

## 5. WARNING

1. `ADR-001` 번호는 현재 `develop` 기준 첫 ADR이지만 미병합/future ADR registry와 번호 조정이 필요할 수 있습니다.
2. `risk`, `approved`, `training_allowed`, `runtime_allowed`를 boolean 하나로 축약하면 안전 경계를 잃습니다.
3. FeatureRecord의 melody/embedding이 원본 재식별 또는 복원 가능성을 높일 수 있어 별도 privacy·rights 검토가 필요합니다.
4. Similarity threshold는 calibration·정책·법무 검토 전 확정하면 안 됩니다.

## 6. 검증 결론

공통 객체는 기존 제안 용어와 대체로 양립하지만 Manifest 역할과 branch 통합 순서는 미결정입니다. 이번 PR은 이를 `[제안]`과 blocker로 유지하며 실제 구현·migration을 승인하지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | develop 및 두 미병합 문서 브랜치와 용어·역할·통합 위험 비교 |
