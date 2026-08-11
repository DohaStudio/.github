# DatasetVersion Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`DatasetVersion`은 승인된 LearningCandidate를 특정 task와 split로 동결한 불변 학습 입력입니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `dataset_id` | 논리 Dataset ID |
| `dataset_version` | 불변 version |
| `task` | 단일 task 또는 명시적 multi-task manifest |
| `lineage` | candidate·source·processing reference |
| `created_from` | LearningCandidate ID 집합 fingerprint |
| `candidate_count` | 포함 candidate 수 |
| `split_manifest` | train/validation/test와 group policy |
| `schema_manifest_id` | record schema identity |
| `rights_summary` | 권리·consent 집계와 예외 0건 증거 |
| `approved` | Dataset 사용 승인 |
| `frozen` | content/split/checksum 동결 |
| `training_allowed` | 특정 목적 학습 허용 |
| `content_fingerprint` | 정렬·직렬화 규칙이 고정된 checksum |
| `supersedes` | 대체 이전 version |

`schema_name`은 `dataset_version`입니다.

## 3. 불변 조건

- 모든 candidate는 `approved` 및 TrainingEligibility 통과 상태여야 합니다.
- `approved`, `frozen`, `training_allowed`가 모두 true여야 TrainingRun 입력이 됩니다.
- split은 source/user/project/reference group 누수를 차단합니다.
- item, preprocessing, split 또는 권리 판단 변경은 새 dataset version을 발급합니다.
- Reference Audio binary·URI와 재현 가능한 원본 표현을 payload에 포함하지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | candidate 기반 불변 Dataset version과 승인·동결·학습 Gate 정의 |
