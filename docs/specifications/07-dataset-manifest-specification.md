# 07. Dataset Manifest 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어

## 1. 목적

Dataset Manifest는 Dataset의 identity, version, source, 권리, split, checksum과 lifecycle을 기록합니다. 실제 Dataset 파일과 개인 경로는 Manifest 공개본에 포함하지 않습니다.

## 2. 최소 필드

| 필드 | 의미 |
|---|---|
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
| `content_checksum_set_id` | item checksum 집합 식별자 |
| `split_id` | 고정 split 정의 식별자 |
| `created_at` | Manifest 생성 시각 |
| `supersedes_dataset_version` | 대체하는 이전 version. 없을 수 있음 |
| `deletion_status` | 삭제·철회 처리 상태 |

## 3. 권리 상태

`training_allowed`는 최소 `true`, `false`, `pending_review`를 표현합니다. `commercial_usage_status`는 `research_only`, `commercial_review_pending`, `commercial_approved`, `commercial_rejected`를 사용할 수 있습니다.

Dataset level 승인은 item level 권리, Consent와 목적별 승인을 대체하지 않습니다. 본인 음성에도 반주·가사·제3자 저작물 권리가 별도로 적용될 수 있습니다.

## 4. 데이터 분할

Split은 `train`, `validation`, `test`와 필요 시 domain 확장 집합을 정의합니다. 동일 source, speaker, 작품 또는 중복 content가 여러 split에 누수되지 않도록 group 기준과 생성 algorithm version을 기록합니다.

## 5. 공개·비공개 분리

공개 가능한 Manifest에는 비식별 ID, 안전한 source alias, 검토 상태와 checksum을 기록할 수 있습니다. 실제 파일명, 절대 경로, 개인 연락처, Consent 증적과 비공개 Review는 private companion record에 둡니다.

## 6. 불변과 변경

Dataset item, split, 전처리 또는 권리 판단이 달라지면 새 `dataset_version`을 발급합니다. 기존 Manifest를 소급 수정하지 않고 대체 관계와 변경 이유를 기록합니다.

## 7. Git 정책

- Schema, 설정 예제, 권리 검토 양식과 합법적 소형 fixture는 Git에 포함할 수 있습니다.
- 원본·전처리 Dataset, 개인 음성, AIHub package, cache와 실제 private Manifest는 Public Git에 포함하지 않습니다.

## 관련 명세

- [Model Manifest 명세](06-model-manifest-specification.md)
- [Storage Layout 명세](09-storage-layout-specification.md)
- [공통 용어](10-common-terms.md)
