# 02. AssetVersion 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 정의

AssetVersion(자산 버전)은 Asset의 특정 시점 상태를 나타내는 불변 객체입니다. 내용, 참조 Artifact, 처리 설정 또는 계보가 달라지면 기존 Version을 수정하지 않고 새 Version을 생성합니다.

## 2. 불변 원칙

- 생성된 AssetVersion의 내용과 계보 필드는 수정하지 않습니다.
- 정정, 재처리, 사용자 편집과 최종 선택은 모두 새 Version을 만듭니다.
- Metadata 오류를 정정해야 하면 감사 이력을 보존하고 정정 Version 또는 별도 관리 Metadata를 사용합니다.
- 삭제·보존 상태 변경은 내용 변경이 아니라 lifecycle event로 기록합니다.

## 3. 최소 필드

| 필드 | 의미 |
|---|---|
| `asset_version_id` | 불변 Version 식별자 |
| `asset_id` | 상위 Asset 식별자 |
| `version_number` | Asset 내부의 단조 증가 Version 번호 |
| `version_origin` | Version 생성 원인 |
| `source_asset_version_ids` | 직접 입력 Version 목록 |
| `parent_asset_version_id` | 같은 Asset 안의 직접 이전 Version. 없을 수 있음 |
| `artifact_ids` | 참조 Artifact 식별자 목록 |
| `processing_chain_id` | 처리 단계 snapshot 식별자 |
| `provider_id` | 생성 Provider. 사용자 작성이면 없을 수 있음 |
| `model_manifest_id` | 사용 모델 Manifest. 모델 미사용이면 없음 |
| `settings_snapshot` | 생성 시점의 불변 설정 |
| `created_by` | 사용자 또는 시스템 actor |
| `created_at` | 생성 시각 |

## 4. Version 생성 원인

`version_origin`은 최소한 다음 원인을 표현할 수 있어야 합니다.

- `user_created`: 사용자 최초 작성·녹음
- `ai_generated`: AI가 새 결과 생성
- `ai_candidate`: AI 수정·보정 후보
- `user_edited`: 사용자 편집
- `provider_processed`: Provider 기술 처리
- `final_selected`: 사용자가 최종 선택한 상태를 보존한 Version
- `imported`: 외부 결과를 검증 후 가져옴

## 5. 후보와 선택

여러 후보 Version은 동일한 parent를 참조할 수 있습니다. 후보 생성은 원본과 다른 후보를 변경하거나 삭제하지 않습니다. 최종 선택은 Asset의 Selection이 해당 Version을 참조하도록 DohaMusic에서 수행합니다.

## 6. Provider 출력

Provider Job은 성공 시 새 출력 Artifact와 Version 생성에 필요한 Metadata를 반환합니다. Provider가 Workspace DB의 기존 AssetVersion을 직접 수정하지 않습니다. 실패·취소 Job은 입력 Version과 기존 성공 결과에 영향을 주지 않습니다.

## 7. 무결성

- Version 번호와 ID의 유일성을 검증합니다.
- 모든 `artifact_ids`는 checksum이 검증된 Artifact를 가리켜야 합니다.
- 모든 source/parent 참조는 순환하지 않아야 합니다.
- 재시도 결과는 이전 Job과 별도 Version 후보로 식별합니다.

## 관련 명세

- [Asset 명세](01-asset-specification.md)
- [Artifact 명세](03-artifact-specification.md)
- [Job 계약](05-job-contract.md)
- [Composition Snapshot 명세](08-composition-snapshot-specification.md)
