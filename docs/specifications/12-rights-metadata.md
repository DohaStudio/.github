# RightsMetadata Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`RightsMetadata`는 source의 생성·업로드 유형과 분석·학습·재배포·보관의 목적별 허용 상태를 기록합니다. 기술적 가능성과 권리 허용을 분리합니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `rights_metadata_id` | immutable 권리 record ID |
| `source_type` | source 분류 |
| `rights_status` | 검토 상태 |
| `user_created` | 사용자 창작 여부와 evidence ref |
| `generated` | AI 생성 여부와 provider/model ref |
| `reference` | reference 용도 여부 |
| `uploaded` | 업로드 source 여부 |
| `external` | 외부 source/provider 여부 |
| `analysis_allowed` | 분석 목적 허용 |
| `training_allowed` | 학습 목적 허용 |
| `redistribution_allowed` | 원본/파생 공개 허용 |
| `retain_source` | 원본 보관 허용과 기간 |
| `consent_evidence_refs` | 비공개 consent evidence 참조 |
| `jurisdiction` | 적용 지역·정책 context |
| `reviewed_at`, `reviewed_by` | 검토 evidence |

`schema_name`은 `rights_metadata`입니다. `source_type`은 `user_created`, `generated`, `reference`, `uploaded`, `external`, `mixed`를 사용합니다. `rights_status`는 `unknown`, `pending_review`, `approved_limited`, `approved`, `rejected`, `revoked`를 사용합니다.

## 3. 불변 조건

- `unknown`, `pending_review`, `rejected`, `revoked`는 학습을 fail closed합니다.
- `analysis_allowed`는 `training_allowed`를 의미하지 않습니다.
- `retain_source=false`여도 승인된 파생 feature 보관 여부는 별도 필드·목적으로 검토합니다.
- Dataset/Model approval이 item-level RightsMetadata를 덮어쓰지 않습니다.
- Consent 원문·개인정보·로컬 경로는 공개 객체에 넣지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | source type과 분석·학습·재배포·retention 권리 분리 정의 |
