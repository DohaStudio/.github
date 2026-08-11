# RevisionPlan Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`RevisionPlan`은 SimilarityReport 또는 Music QA 결과를 DohaLM이 실행 가능한 수정 의도로 변환한 계획입니다. 계획은 사용자 승인 전 실제 자산을 변경하지 않습니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `revision_plan_id` | immutable ID |
| `source_similarity_report_id` | 원인이 된 SimilarityReport |
| `source_asset_version_id` | 수정 전 불변 version |
| `preserve` | 유지할 음악 요소·구간 |
| `replace` | 교체할 음악 요소·구간 |
| `steps` | 순서가 있는 수정 단계 |
| `approval_status` | `proposed`, `approved`, `rejected`, `superseded` |
| `expected_effect` | similarity/quality에 기대하는 영향과 한계 |

`schema_name`은 `revision_plan`입니다.

각 `steps[]`는 `step_id`, `target_track`, `target_section`, `instruction`, `priority`, `expected_effect`, `provider_capability_id`, `depends_on`을 포함합니다.

## 3. 불변 조건

- `preserve`와 `replace`가 같은 대상을 포함하면 거부합니다.
- 모든 step은 기존 AssetVersion의 track/section identity를 참조합니다.
- 순환 dependency가 있으면 거부합니다.
- 실행 전 각 step을 [MusicIntent](01-music-intent.md)로 materialize하고 사용자/정책 승인을 확인합니다.
- Revision 결과는 새 AssetVersion이며 원본을 덮어쓰지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | similarity 기반 preserve/replace와 단계별 수정 계획 정의 |
