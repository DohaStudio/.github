# TrainingRun Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`TrainingRun`은 고정 DatasetVersion, base model과 설정에서 수행되는 단일 학습 실행 identity입니다. 이 명세는 학습 실행을 승인하지 않습니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `training_run_id` | immutable run ID |
| `dataset_version_ref` | DatasetVersion identity·fingerprint |
| `dataset_manifest_id` | DatasetVersion과 결속된 issued Manifest |
| `base_model_version_id` | parent ModelVersion |
| `adapter_strategy` | none/LoRA/QLoRA/기타 명시적 전략 |
| `hyperparameters` | resolved immutable 설정 reference |
| `seed` | data/model/runtime seed 집합 |
| `source_commit` | 실행 코드 commit |
| `environment_manifest_id` | hardware·framework·dependency identity |
| `status` | run lifecycle |
| `checkpoint_refs` | 중간·최종 checkpoint artifact |
| `metrics_refs` | training metric artifact |
| `failure` | 실패 code·stage·safe summary |

`schema_name`은 `training_run`입니다. canonical 실행 상태는 `queued`, `running`, `succeeded`, `failed`, `cancelled`입니다. 실행 승인과 Dataset Gate는 별도 evidence이며 실행 상태 enum에 섞지 않습니다.

## 3. 불변 조건

- DatasetVersion의 세 Gate와 RightsMetadata 목적 범위가 모두 유효해야 합니다.
- DatasetVersion/Manifest stable ID·schema version·checksum 결속이 검증돼야 합니다.
- 실행 후 Dataset, base, hyperparameter, seed identity를 변경하지 않습니다.
- 자동 retry는 새 TrainingRun ID를 사용합니다.
- `succeeded`는 실행 성공만 뜻하며 성능 승인이나 Runtime 사용 허용을 뜻하지 않습니다.
- terminal 상태 `succeeded`, `failed`, `cancelled`의 run record를 제자리 덮어쓰지 않습니다. retry는 새 TrainingRun과 parent attempt reference를 사용합니다.
- checkpoint는 checksum과 parent run을 가져야 합니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | Dataset·base·adapter·hyperparameter·seed와 run lifecycle 정의 |
