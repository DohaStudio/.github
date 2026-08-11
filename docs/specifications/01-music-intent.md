# MusicIntent Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`MusicIntent`는 DohaLM이 해석·생성하고 DohaMusic이 orchestration하며 DohaAudio·DohaVocal이 실행 가능한 형태로 소비하는 공통 음악 작업 의도입니다.

## 2. 필수 필드

| 필드 | 형식 | 의미 |
|---|---|---|
| `intent_id` | string | immutable intent ID |
| `operation` | enum | 요청 작업 |
| `target` | object | project/asset/track/section과 정확한 version reference |
| `instruction` | string 또는 structured reference | 수행할 작업의 의미 |
| `preserve` | string[] | 보존해야 하는 요소 |
| `replace` | string[] | 교체 가능한 요소 |
| `constraints` | object[] | 길이·장르·음역·권리·provider 제약 |
| `priority` | enum | `low`, `normal`, `high`, `critical` |
| `requested_capability` | capability ID | 필요한 [ProviderCapability](11-provider-capability.md) |

공통 Envelope의 `schema_name`은 `music_intent`입니다.

## 3. Operation

`regenerate`, `replace`, `extend`, `shorten`, `rewrite`, `mix`, `analyze`, `reference`, `similarity_revision`, `planning`을 정의합니다. 저장소별 operation은 `extensions.<namespace>`에 추가하며 공통 enum으로 가장하지 않습니다.

## 4. Target

| 필드 | 필수 | 의미 |
|---|---:|---|
| `project_id` | 예 | DohaMusic project |
| `asset_version_id` | 조건부 | 기존 자산 대상일 때 고정 version |
| `track_id` | 조건부 | track 범위 작업 |
| `section_id` | 조건부 | section 범위 작업 |
| `time_range` | 아니오 | 명시적 시간 범위와 단위 |

`track_id`, `section_id`, `time_range`가 함께 있을 때 범위가 서로 모순되면 거부합니다.

## 5. 불변 조건

- `preserve`와 `replace`에 같은 경로가 있으면 안 됩니다.
- `reference` operation은 승인된 ReferenceAnalysis 또는 source reference가 필요합니다.
- `similarity_revision`은 SimilarityReport와 RevisionPlan reference가 필요합니다.
- 실행 Provider가 capability 또는 schema major version을 지원하지 않으면 실패합니다.
- MusicIntent는 실행 결과가 아니며 기존 AssetVersion을 제자리 수정하지 않습니다.

## 6. 예시

```yaml
schema_name: music_intent
schema_version: 1.0.0
object_id: intent_01
intent_id: intent_01
operation: replace
target:
  project_id: project_01
  asset_version_id: asset_version_07
  track_id: track_vocal
  section_id: chorus_02
instruction: 후렴의 마지막 두 마디를 더 짧고 상승하는 선율로 교체
preserve: [lyrics, singer_identity, section_length]
replace: [vocal_melody]
constraints: []
priority: normal
requested_capability: vocal_melody_edit
created_at: 2026-08-11T00:00:00Z
created_by: user_opaque
```

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 공통 operation, target, preserve/replace, instruction·constraint 정의 |
