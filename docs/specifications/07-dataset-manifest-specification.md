# 07. Dataset Manifest 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 목적

DatasetManifest는 권위 [DatasetVersion](07-dataset-version.md)을 재현하는 불변 직렬화 evidence입니다. 실제 포함 item, split, object/file/Artifact reference, checksum/digest, 생성 도구와 형식 version을 기록하며 DatasetVersion과 경쟁하는 approval·lifecycle source of truth가 아닙니다.

## 2. 최소 필드

| 필드 | 의미 |
|---|---|
| `dataset_manifest_id` | immutable Manifest ID |
| `manifest_status` | 발행 전 `draft` 또는 terminal `issued` |
| `manifest_format_version` | 직렬화 형식 version |
| `source_dataset_version_id` | 권위 DatasetVersion stable ID |
| `source_dataset_version_checksum` | Version/Manifest 결속 digest |
| `producer` | 생성 도구·version |
| `dataset_id` | Dataset 논리 식별자 |
| `dataset_version` | 불변 Dataset version |
| `dataset_domain` | `lm`, `audio`, `vocal` 등의 도메인 |
| `source` | 공급자·수집 경로를 식별하는 안전한 출처 Metadata |
| `license_status` | Dataset license 검토 상태 |
| `training_allowed` | 학습 사용 허용 상태 |
| `commercial_usage_status` | 상업 이용 검토 상태 |
| `redistribution_allowed` | 원본·파생 Metadata 재배포 허용 상태 |
| `item_count` | Dataset item 수 |
| `manifest_checksum` | Manifest 자체 checksum |
| `object_file_artifact_refs` | 포함 item의 안전한 물리 reference |
| `content_checksum_set_id` | item checksum 집합 식별자 |
| `split_id` | 고정 split 정의 식별자 |
| `created_at` | Manifest 생성 시각 |
| `supersedes` | 공식 replacement가 대체하는 이전 Manifest ID |
| `deletion_status` | 발행 시점 삭제·철회 상태 snapshot; 후속 변경은 append-only event |

## 3. 권리 상태

`training_allowed`는 source DatasetVersion의 발행 시점 snapshot이며 독립 승인 필드가 아닙니다. `commercial_usage_status`도 권위 rights/approval evidence의 snapshot입니다. Manifest가 두 상태를 독립적으로 변경할 수 없습니다.

Dataset level 승인은 item level 권리, Consent와 목적별 승인을 대체하지 않습니다. 본인 음성에도 반주·가사·제3자 저작물 권리가 별도로 적용될 수 있습니다.

## 4. 데이터 분할

Split은 `train`, `validation`, `test`와 필요 시 domain 확장 집합을 정의합니다. 동일 source, speaker, 작품 또는 중복 content가 여러 split에 누수되지 않도록 group 기준과 생성 algorithm version을 기록합니다.

## 5. 공개·비공개 분리

공개 가능한 Manifest에는 비식별 ID, 안전한 source alias, 검토 상태와 checksum을 기록할 수 있습니다. 실제 파일명, 절대 경로, 개인 연락처, Consent 증적과 비공개 Review는 private companion record에 둡니다.

## 6. 불변과 변경

`draft`는 발행 전 검토 중에만 변경할 수 있습니다. `issued` DatasetManifest는 terminal immutable record입니다. payload, 포함 Candidate/Sample, split, object/file/Artifact reference, checksum/digest, 생성 도구·format version 또는 source DatasetVersion 중 하나라도 달라지면 같은 Manifest ID를 유지할 수 없습니다.

Dataset 구성이나 권리 판단이 달라지면 새 DatasetVersion과 새 DatasetManifest를 발급합니다. 논리 DatasetVersion은 같지만 발행 evidence 오류를 정정해야 하는 예외는 새 Manifest ID와 canonical `supersedes` 관계를 사용하며 source DatasetVersion approval을 변경할 수 없습니다. 기존 Version·Manifest를 삭제하거나 덮어쓰지 않습니다.

같은 source DatasetVersion의 issued replacement는 root와 tip이 각각 하나인 단일 선형 `supersedes` chain이어야 하며 branch, merge, cycle, self-reference, 누락되거나 분리된 predecessor를 허용하지 않습니다.

## 7. Git 정책

- Schema, 설정 예제, 권리 검토 양식과 합법적 소형 fixture는 Git에 포함할 수 있습니다.
- 원본·전처리 Dataset, 개인 음성, AIHub package, cache와 실제 private Manifest는 Public Git에 포함하지 않습니다.

## 관련 명세

- [Model Manifest 명세](06-model-manifest-specification.md)
- [Storage Layout 명세](09-storage-layout-specification.md)
- [공통 용어](10-common-terms.md)
