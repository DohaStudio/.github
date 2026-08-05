# 10. 공통 용어와 공식 문서 언어

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 공식 문서 언어 정책

앞으로 DohaStudio 모든 Repository의 Markdown 문서는 한국어를 공식 설명 언어로 사용합니다. README, Roadmap, ADR, Architecture, Requirements, Database, Security, Guide와 Contribution 문서의 설명 문장은 한국어로 작성합니다.

다음 항목은 영문을 유지할 수 있습니다.

- 코드와 code block
- API, 클래스명, 함수명과 field name
- 파일명과 경로
- 표준 기술 용어와 고유 제품명
- Git Commit Prefix와 Branch 이름
- Schema enum과 protocol identifier

올바른 표현 예시는 `Asset is immutable.`이 아니라 `AssetVersion(자산 버전)은 불변입니다.`입니다. 영문 기술 용어를 처음 사용할 때는 가능한 경우 한국어 의미를 함께 설명합니다.

이 정책은 기존 영문 문서를 이번 작업에서 일괄 변경한다는 의미가 아닙니다. 새 문서와 실질적으로 수정하는 기존 문서부터 단계적으로 적용하며, 코드·계약 식별자의 호환성을 깨뜨리는 번역은 하지 않습니다.

## 2. 핵심 용어

| 용어 | 한국어 설명 |
|---|---|
| `Asset` | Workspace 범위에서 관리되고 `ProjectAsset`을 통해 여러 Project에서 재사용할 수 있는 논리 자산. 실제 파일이 아님 |
| `AssetVersion` | Asset의 특정 시점 불변 상태와 계보 |
| `Artifact` | 실제 파일 또는 직렬화된 Payload |
| `AssetRelation` | Asset 또는 Version 사이의 의미 관계 |
| `Workspace` | 사용자·Project·권한·Asset·Job·결과를 관리하는 제품 영역 |
| `Project` | 하나의 음악 작품과 관련 Workspace 상태를 묶는 단위 |
| `Composition Snapshot` | 선택된 AssetVersion과 처리·Provider·Model version을 고정한 불변 구성 |
| `Provider` | DohaMusic이 호출하는 독립 AI 기능 제공자 |
| `Capability` | Provider가 지원하는 생성·분석·변환 등의 기능 식별자 |
| `Job` | 비동기 작업 요청, 상태와 결과의 lifecycle 단위 |
| `Manifest` | Dataset·Model 등의 identity, version, provenance와 검증 근거를 기록한 불변 Metadata |
| `Registry` | 여러 Manifest와 상태·관계를 조회하는 관리 index |
| `Artifact ID` | 물리 경로와 분리된 Artifact 식별자 |
| `Model Manifest` | 모델·Checkpoint·Dataset·Training·Evaluation·License를 연결한 명세 |
| `Dataset Manifest` | Dataset version·source·rights·split·checksum을 연결한 명세 |
| `Checkpoint` | Training 중간 또는 최종 모델 상태 Artifact |
| `Runtime` | Model을 load하고 Provider Job을 실행하는 환경·process |
| `Adapter` | 모델 전체를 바꾸지 않고 특정 사용자·task에 맞춘 parameter 또는 구현 계층 |
| `Take` | 같은 Recording 목적에서 생성된 개별 녹음 시도 |
| `Recording` | 사용자가 녹음한 원본 또는 작품 입력 자산 |
| `Enrollment` | 음색 등록·참조를 위한 별도 승인 sample과 처리 과정 |
| `Training Dataset` | 명시적으로 학습 사용 승인을 받은 Dataset. Recording·Enrollment와 자동 동일하지 않음 |
| `Selection` | 여러 AssetVersion 후보 중 Workspace가 현재 채택한 Version |
| `Approval` | 목적별 사용 허용 판단과 근거 |
| `Lineage` | source, parent, processing, Dataset, Model과 Run의 파생 계보 |
| `Commercial Review` | 상업 이용 조건과 권리 근거를 별도로 검토하는 Gate |
| `Legacy` | 현재 계약 이전의 호환 대상. 완료·권장 상태를 의미하지 않음 |

## 3. Repository 용어 경계

- DohaMusic은 Workspace, Project, Asset, AssetVersion, Composition Snapshot, Mix와 Export를 소유합니다.
- DohaLM은 Lyrics 생성·분석·수정 Provider 도메인을 소유합니다.
- DohaAudio는 Music generation, Stem separation과 Audio analysis Provider 도메인을 소유합니다.
- DohaVocal은 Singing voice, Voice conversion과 Vocal processing Provider 도메인을 소유합니다.
- Provider끼리는 직접 호출하지 않으며 DohaMusic이 orchestration합니다.

## 4. 용어 사용 규칙

- Asset와 Artifact를 서로 바꾸어 쓰지 않습니다.
- Asset와 AssetVersion을 서로 바꾸어 쓰지 않습니다.
- Asset에 `project_id`를 두지 않으며 Project와 Asset은 `ProjectAsset`으로 연결합니다.
- Snapshot은 Asset의 최신 상태가 아니라 정확한 AssetVersion을 참조합니다.
- Recording Take와 Enrollment Sample을 Training Dataset으로 자동 간주하지 않습니다.
- Evaluation 통과와 Commercial approval을 같은 상태로 표현하지 않습니다.
- `Legacy`를 삭제 완료 또는 안전 검증 완료 의미로 사용하지 않습니다.

## 5. Specification 목록

1. [Asset 명세](01-asset-specification.md)
2. [AssetVersion 명세](02-asset-version-specification.md)
3. [Artifact 명세](03-artifact-specification.md)
4. [Provider 계약](04-provider-contract.md)
5. [Job 계약](05-job-contract.md)
6. [Model Manifest 명세](06-model-manifest-specification.md)
7. [Dataset Manifest 명세](07-dataset-manifest-specification.md)
8. [Composition Snapshot 명세](08-composition-snapshot-specification.md)
9. [Storage Layout 명세](09-storage-layout-specification.md)
