# AI Music Common Contracts 문서 정합성 검토

> 상태: [검토]
> 마지막 검토일: 2026-08-11
> 비교 기준: 원격 `develop` `80f965a`, `main` `1e4b480`, PR #5 작업 전 head `f6cd5fc`

## 1. 기준 상태

- PR #1 `docs/bootstrap-organization → develop`은 merge commit `ff30c55`로 병합됐습니다.
- PR #2 `docs/specifications → develop`은 merge commit `a32a4d8`로 병합됐습니다.
- PR #3 `stabilize/organization-baseline → develop`은 merge commit `80f965a`로 병합됐습니다.
- PR #5는 작업 전 최신 `develop`과 `CONFLICTING/DIRTY`였으며 `origin/develop` merge로 기준선 이력을 보존했습니다. 충돌은 `README.md`, `docs/index.md`, `docs/specifications/README.md` 3개였고 기존 조직 기준선을 유지한 확장 링크 방식으로 해소했습니다.
- `docs/bootstrap-organization`, `docs/specifications` 원격 branch tip은 존재하지만 연결된 PR #1·#2는 모두 merged이고 현재 Open PR은 #5뿐입니다. PR #5는 branch tip의 후속 미병합 commit에 의존하지 않습니다.

## 2. 용어 정합성

| 새 객체 | 기존 미병합 용어 | 판정 | 통합 규칙 |
|---|---|---|---|
| MusicIntent | AssetVersion, Composition Snapshot, Provider Capability | compatible | target은 정확한 AssetVersion을 참조 |
| ProviderCapability | Provider Contract의 `Capability` | compatible_extension | discovery 객체로 역할 구체화 |
| DatasetVersion | Dataset Manifest | authority_resolved | Version이 논리 source of truth, Manifest는 immutable reproduction evidence |
| ModelVersion | Model Manifest | authority_resolved | Version이 논리 source of truth, Manifest는 immutable deployment evidence |
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
| Lineage | Candidate→Eligibility→DatasetVersion→DatasetManifest→Training→Evaluation→ModelVersion→ModelManifest→Runtime 추적 정의 |

## 4. 해결한 Blocker

1. 선행 PR #1·#2·#3의 `develop` 병합을 GitHub에서 확인하고 최신 base를 feature branch에 merge했습니다.
2. DatasetVersion/ModelVersion을 논리 권위로, DatasetManifest/ModelManifest를 발행 후 immutable evidence로 확정했습니다.
3. ADR 번호를 `develop`과 전체 Open/Merged PR에서 검색했고 기존 ADR 파일이 없어 ADR-001을 유지했습니다.
4. TrainingEligibility에서 Runtime 책임을 제거하고 Dataset 집합 Gate와 Model Runtime Gate를 분리했습니다.

현재 문서 계약 범위의 활성 blocker는 0건입니다. JSON Schema·validator·fixture와 Repository mapping은 production 호환성의 후속 조건이지만 이번 문서 PR Ready 전환 blocker는 아닙니다.

## 5. WARNING

1. FeatureRecord의 melody/embedding은 원본 재식별 또는 추론 위험이 있어 storage·access·retention 권한을 원본과 분리해야 합니다.
2. Similarity threshold는 calibration·정책·법무 검토 전 확정하면 안 되며 저작권 침해 법적 판정으로 사용하지 않습니다.
3. Rights revocation 이후 파생 Dataset/Model 처리는 append-only event와 replacement lineage를 따르지만 상세 운영 정책은 후속 결정입니다.
4. Provider capability version negotiation, JSON Schema·Compatibility Validator, artifact retention과 기존 DohaLM REST/SSE compatibility 검증은 후속 범위입니다.

## 6. 검증 결론

선행 기준선은 최신 `develop` merge로 통합됐고 Common Contracts는 기존 Asset·Artifact·Job·Provider 계약의 확장으로 정렬됐습니다. Version/Manifest 권위, Candidate/Dataset/Runtime Gate, Owner, lifecycle과 immutability의 활성 문서 모순은 정적 검색 결과 0건입니다. 이번 PR은 문서 계약만 승인 대상으로 하며 실제 Schema·Runtime·Dataset·migration을 승인하지 않습니다.

## 7. 최종 정적 검증

2026-08-11에 병합 결과 전체 Markdown 53개를 대상으로 다음 검사를 실행했습니다.

- UTF-8 strict decode, local Markdown link target, code fence, Mermaid 시작 구문, YAML/JSON example parse: 오류 0건
- heading anchor 중복, Markdown table 최소 구조, trailing whitespace, Windows absolute-path link: 오류 0건
- conflict marker, 1 MiB 초과 파일, private key·GitHub token·AWS access key·일반 secret assignment 패턴: 탐지 0건
- `git diff --check`: 오류 0건

이 검사는 문서의 구조·참조·정적 계약 모순을 검증하며, 아직 구현하지 않은 JSON Schema validator나 Provider Runtime integration test를 대신하지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 53개 Markdown 링크·구문·인코딩·secret·large-file·conflict-marker 정적 검증 통과 |
| 2026-08-11 | PR #1·#2·#3 병합 확인, develop 통합, Version/Manifest·Gate·Owner·immutability 최종 검토 |
