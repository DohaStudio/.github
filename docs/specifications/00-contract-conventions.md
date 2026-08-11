# AI Music Common Contract 공통 규칙

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 적용 범위

모든 공통 객체는 transport와 저장 기술에 독립적입니다. 구현체는 필드 이름·enum 의미·불변 조건을 유지해야 하며 저장소 전용 필드는 `extensions` 아래에 둡니다.

## 2. 공통 Envelope

| 필드 | 형식 | 필수 | 의미 |
|---|---|---:|---|
| `schema_name` | string | 예 | Specification의 고정 이름 |
| `schema_version` | semver string | 예 | 객체 schema version |
| `object_id` | opaque string | 예 | 전역 충돌을 피하는 immutable ID |
| `created_at` | RFC 3339 UTC | 예 | 생성 시각 |
| `created_by` | actor reference | 예 | user/service/reviewer 식별자 |
| `extensions` | object | 아니오 | namespace가 있는 저장소별 확장 |

ID는 로컬 경로·이메일·원문에서 파생하지 않습니다. 공개 객체에는 비밀, 개인정보와 절대 경로를 넣지 않습니다.

## 3. Versioning

- field 추가처럼 기존 소비자가 무시할 수 있는 변경은 minor version을 올립니다.
- field 삭제, enum 의미 변경, 필수 조건 강화는 major version을 올립니다.
- 이미 발급된 객체를 소급 변경하지 않고 새 객체나 새 version을 발급합니다.
- 소비자는 지원하지 않는 major version을 fail closed로 거부합니다.

## 4. 공통 상태 원칙

- lifecycle 상태와 권리 상태를 합치지 않습니다.
- `approved`는 검토 승인이고 `training_allowed` 또는 `runtime_allowed`를 자동 의미하지 않습니다.
- 실패·거절·deprecated 객체도 lineage 감사 목적으로 보존합니다.
- `null`, 누락과 `false`를 같은 의미로 처리하지 않습니다.

## 5. 참조와 Lineage

객체 관계는 embedded payload보다 ID reference를 우선합니다. 참조 대상의 `object_id`, `schema_version`, 필요 시 `content_fingerprint`를 기록합니다. Lineage는 source → candidate → dataset → run → model → runtime 방향으로 추적 가능해야 합니다.

## 6. 검증 공통 오류

| 오류 | 조건 |
|---|---|
| `UNSUPPORTED_SCHEMA_VERSION` | 지원하지 않는 major version |
| `MISSING_REQUIRED_FIELD` | 필수 필드 누락 |
| `INVALID_ENUM_VALUE` | 정의되지 않은 enum |
| `INVALID_REFERENCE` | 대상 identity·type 불일치 |
| `RIGHTS_GATE_NOT_PASSED` | 요청 목적에 필요한 권리 미승인 |
| `LINEAGE_INCOMPLETE` | 필수 parent/source 누락 |
| `STATE_TRANSITION_INVALID` | 허용되지 않은 lifecycle 전이 |

## 7. 비목표

HTTP endpoint, ORM, DB table, queue, worker, serialization library와 Repository 내부 class 이름은 정의하지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 공통 envelope, versioning, 상태, lineage와 검증 규칙 정의 |
