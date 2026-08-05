# 01. Asset 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 목적

Asset(자산)은 DohaMusic Workspace가 관리하는 논리적 작품 객체입니다. Asset은 실제 파일이 아니며 하나 이상의 [AssetVersion](02-asset-version-specification.md)을 가집니다. 실제 파일 또는 Payload는 [Artifact](03-artifact-specification.md)로 분리합니다.

## 2. 핵심 엔티티

| 엔티티 | 정의 |
|---|---|
| `Asset` | Project 안에서 식별되는 논리 자산 |
| `AssetVersion` | 특정 시점의 불변 자산 상태 |
| `Artifact` | AssetVersion이 참조하는 실제 파일 또는 Payload |
| `AssetRelation` | Asset 또는 AssetVersion 사이의 의미 관계 |
| `ProjectAsset` | Project와 Asset의 소속·표시 관계 |
| `Owner` | 자산의 소유·관리 주체 |
| `Selection` | 여러 후보 중 Workspace가 선택한 Version 정보 |
| `Approval` | 사용 목적별 검토·승인 상태와 근거 |

## 3. Asset 최소 필드

| 필드 | 의미 |
|---|---|
| `asset_id` | 전역 또는 Workspace 범위에서 유일한 식별자 |
| `project_id` | 소속 Project 식별자 |
| `asset_type` | `lyrics`, `music`, `vocal`, `stem`, `recording`, `mix`, `export` 등의 논리 유형 |
| `owner_id` | Owner 식별자 |
| `lifecycle_status` | 현재 lifecycle 상태 |
| `selected_asset_version_id` | 사용자가 선택한 Version 식별자. 없을 수 있음 |
| `created_at` | 생성 시각 |
| `updated_at` | Asset Metadata의 최종 변경 시각 |

## 4. 소유와 책임

Asset과 ProjectAsset의 최종 소유자는 DohaMusic입니다. DohaLM, DohaAudio와 DohaVocal은 Job 결과와 Artifact를 반환할 수 있지만 Workspace Asset을 직접 생성·선택·승인하는 권한을 갖지 않습니다.

Owner는 사용자, Workspace 또는 정책상 허용된 조직 주체를 식별합니다. Provider ID를 Owner로 사용하지 않습니다.

## 5. Lifecycle

공통 lifecycle 후보는 `draft`, `active`, `archived`, `deletion_requested`, `deleted`입니다. `deleted`는 물리 파일 삭제 완료를 자동으로 의미하지 않으며 Artifact와 파생 계보의 삭제 상태를 별도로 확인해야 합니다.

## 6. Selection과 Approval

- Selection은 후보 Version 중 Workspace가 현재 채택한 Version을 가리킵니다.
- 새 후보 생성은 기존 Selection을 자동으로 변경하지 않습니다.
- Approval은 `usage_purpose`, `status`, `approved_by`, `evidence_id`, `decided_at`을 기록해야 합니다.
- 평가 통과, 사용자 선택, 학습 허용과 상업 이용 승인은 서로 다른 결정입니다.

## 7. AssetRelation

AssetRelation은 `relation_id`, `source_id`, `target_id`, `relation_type`, `created_at`을 가집니다. `derived_from`, `alternative_of`, `component_of`, `replaces` 등의 관계를 사용할 수 있으나 구체 enum은 Repository 계약에서 versioning합니다.

## 8. 금지 사항

- Asset에 로컬 절대 파일 경로를 저장하지 않습니다.
- Asset와 Artifact를 같은 ID 공간으로 취급하지 않습니다.
- Provider가 사용자의 최종 Selection이나 Approval을 임의로 변경하지 않습니다.
- 논리 삭제만으로 개인 데이터의 물리 삭제가 완료됐다고 표시하지 않습니다.

## 관련 명세

- [AssetVersion 명세](02-asset-version-specification.md)
- [Artifact 명세](03-artifact-specification.md)
- [Composition Snapshot 명세](08-composition-snapshot-specification.md)
- [공통 용어](10-common-terms.md)
