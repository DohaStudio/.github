# SimilarityReport Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`SimilarityReport`는 생성 음악과 승인된 Reference Feature 사이의 유사도를 설명하는 창작 지원 객체입니다. 법률 의견, 저작권 침해 판정 또는 표절 단정이 아닙니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `similarity_report_id` | immutable ID |
| `subject_feature_record_id` | 생성 결과 FeatureRecord |
| `reference_feature_record_ids` | 비교 catalog의 승인된 FeatureRecord |
| `metric_manifest_id` | metric·model·weight·threshold version |
| `overall` | 종합 score·confidence·limitations |
| `melody` | melody similarity |
| `vocal_melody` | vocal melody similarity |
| `chord` | chord progression similarity |
| `rhythm` | rhythm similarity |
| `structure` | structure similarity |
| `arrangement` | arrangement similarity |
| `embedding` | embedding similarity |
| `section` | section별 score·근거 구간 |
| `risk` | policy severity와 근거 |
| `recommendation` | 창작 지원 설명 |
| `revision_required` | policy상 수정 검토 필요 여부 |
| `limitations` | 비교 불가·confidence·catalog 한계 |

`schema_name`은 `similarity_report`입니다.

## 3. Risk

`risk.level`은 `unknown`, `low`, `medium`, `high`, `blocked`를 사용합니다. `blocked`는 제품 정책상 자동 진행을 중단한다는 뜻이며 법적 침해 확정이 아닙니다. threshold는 metric version과 calibration evidence에 결속합니다.

## 4. 불변 조건

- 같은 feature/metric major version 또는 명시적 migration 결과만 비교합니다.
- `overall`만으로 revision 또는 권리 결론을 만들지 않습니다.
- section risk에는 대상과 reference의 구간 evidence가 필요합니다.
- `revision_required=true`이면 RevisionPlan 생성 또는 명시적 override review가 필요합니다.
- Report를 학습 정답으로 자동 등록하지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | similarity dimension, risk, recommendation과 비법률 판정 경계 정의 |
