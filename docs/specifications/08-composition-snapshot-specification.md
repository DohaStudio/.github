# 08. Composition Snapshot 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 정의

Composition Snapshot(구성 Snapshot)은 특정 시점의 곡 구성을 재현하기 위해 선택된 AssetVersion, 처리 설정, Provider와 Model version을 고정하는 불변 Workspace 객체입니다.

Snapshot은 Asset의 최신 상태를 간접 참조하지 않고 정확한 `asset_version_id`를 참조합니다.

## 2. 최소 참조

| 영역 | 참조 내용 |
|---|---|
| Lyrics | 선택된 Lyrics AssetVersion |
| Music | Music 또는 Instrumental AssetVersion |
| Vocal | Recording, Generated 또는 Processed Vocal AssetVersion |
| Stem | 사용된 Stem AssetVersion 목록 |
| Processing | processing chain과 settings snapshot |
| Mix | Mix settings와 관련 Mix AssetVersion. 없을 수 있음 |
| Provider | 결과 생성에 사용된 Provider와 contract version |
| Model | Model Manifest ID와 model version |

## 3. 최소 필드

- `composition_snapshot_id`
- `project_id`
- `snapshot_version`
- `lyrics_asset_version_ids`
- `music_asset_version_ids`
- `vocal_asset_version_ids`
- `stem_asset_version_ids`
- `processing_chain_ids`
- `mix_settings_snapshot`
- `provider_versions`
- `model_manifest_ids`
- `created_by`
- `created_at`

## 4. 불변 원칙

- 생성된 Snapshot의 Version 참조와 설정을 변경하지 않습니다.
- 가사, 음악, 보컬, Stem, 처리 또는 Mix가 바뀌면 새 Snapshot을 생성합니다.
- Asset의 `selected_asset_version_id`가 변경돼도 과거 Snapshot은 그대로 재현돼야 합니다.
- Snapshot은 파일 자체가 아니라 논리 객체이며 직렬화본이 필요하면 Artifact로 저장합니다.

## 5. 생성과 선택

DohaMusic만 Composition Snapshot을 생성하고 Workspace 상태로 선택합니다. Provider는 Snapshot을 직접 수정하지 않으며 Job 입력으로 전달된 Snapshot ID와 Version 참조를 읽기 전용으로 사용합니다.

## 6. Mix와 Export

Mix Job은 입력 Snapshot과 Mix settings를 고정하고 출력 Mix AssetVersion을 만듭니다. Export Job은 선택된 Mix 또는 Snapshot에서 WAV·MP3·FLAC 등의 Export AssetVersion을 생성합니다. 결과 파일은 `DohaArtifacts/music`에 보관합니다.

## 7. 검증

- 모든 참조 AssetVersion과 Artifact의 존재·권한·checksum을 확인합니다.
- 참조 Version이 삭제 요청 상태이면 정책에 따라 생성을 차단하거나 명시적 경고를 기록합니다.
- Provider·Model version 누락 시 재현 가능한 Snapshot으로 승인하지 않습니다.

## 관련 명세

- [AssetVersion 명세](02-asset-version-specification.md)
- [Job 계약](05-job-contract.md)
- [Storage Layout 명세](09-storage-layout-specification.md)
