# 03. Artifact 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 정의

Artifact(아티팩트)는 실제 파일 또는 직렬화된 Payload입니다. 예시는 `txt`, `wav`, `mp3`, `flac`, `json`, `yaml`입니다. Artifact는 논리 객체인 Asset이 아니며 [AssetVersion](02-asset-version-specification.md)이 Artifact ID를 참조합니다.

## 2. 최소 메타데이터

| 필드 | 의미 |
|---|---|
| `artifact_id` | 저장 위치와 독립적인 식별자 |
| `artifact_kind` | `lyrics_text`, `audio`, `stem`, `manifest`, `model`, `checkpoint`, `evaluation`, `snapshot` 등의 유형 |
| `media_type` | MIME type 또는 표준 직렬화 형식 |
| `size_bytes` | Payload 크기 |
| `checksum_algorithm` | 기본 권장값 `sha256` |
| `artifact_checksum` | Payload checksum |
| `producer_type` | `user`, `provider`, `workspace`, `import` |
| `producer_id` | Provider 또는 actor 식별자 |
| `run_id` | 생성 Job·Training·Evaluation Run 식별자. 없을 수 있음 |
| `created_at` | 생성 시각 |
| `retention_status` | 보존·삭제 lifecycle 상태 |

## 3. 참조 원칙

- Workspace DB에는 로컬 절대 경로가 아니라 `artifact_id`만 저장합니다.
- Provider API도 Windows 경로나 사용자 profile 경로를 반환하지 않습니다.
- 저장 위치 해석은 별도 Artifact Catalog 또는 Resolver가 담당합니다.
- 외부 교환이 필요하면 승인된 `artifact://` URI 또는 접근 제어된 URI를 사용할 수 있습니다.

## 4. 내용 무결성

Artifact 등록 전에 크기와 checksum을 계산합니다. 같은 ID의 Payload를 덮어쓰지 않습니다. Payload가 달라지면 새 Artifact ID를 발급하고 새 AssetVersion 또는 Manifest에서 참조합니다.

## 5. 유형별 예시

| 도메인 | Artifact 예시 |
|---|---|
| Lyrics | UTF-8 text, 구조화된 JSON |
| Audio | WAV, FLAC, MP3 preview |
| Model | 모델 weight, Adapter, Checkpoint |
| Evaluation | JSON metric, Markdown report |
| Workspace | Mix, Export, Preview, Composition Snapshot |

파일 확장자만으로 Artifact kind를 결정하지 않습니다. MIME type, kind와 계약 version을 함께 사용합니다.

## 6. 보안과 삭제

- Dataset, 개인 음성, Checkpoint와 생성 미디어를 Public Git에 저장하지 않습니다.
- Artifact 접근 권한은 Workspace와 Owner 정책을 따릅니다.
- 논리 삭제, 격리, 물리 삭제와 감사 이력을 구분합니다.
- source/parent 계보가 있는 Artifact를 삭제할 때 영향을 먼저 계산합니다.

## 관련 명세

- [AssetVersion 명세](02-asset-version-specification.md)
- [Storage Layout 명세](09-storage-layout-specification.md)
- [공통 용어](10-common-terms.md)
