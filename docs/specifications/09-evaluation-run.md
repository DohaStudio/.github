# EvaluationRun Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`EvaluationRun`은 TrainingRun 산출물을 고정 metric, dataset과 human review 기준으로 평가하는 독립 실행입니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `evaluation_run_id` | immutable run ID |
| `training_run_id` | 평가 대상 학습 실행 |
| `checkpoint_ref` | 정확한 평가 artifact |
| `evaluation_dataset_version_ids` | 고정 평가 Dataset |
| `metric_manifest_ids` | metric 구현·version·threshold |
| `metric_results` | 수치·confidence·sample count |
| `human_review` | rubric, reviewer, blind 조건과 결과 |
| `similarity_report_ids` | 음악 유사도 평가 결과 |
| `rights_review` | runtime 목적 권리 검토 |
| `status` | `queued`, `running`, `completed`, `failed`, `cancelled` |
| `approval` | `pending`, `approved`, `rejected`와 evidence |
| `limitations` | 대표성·누수·환경 한계 |

`schema_name`은 `evaluation_run`입니다.

## 3. 불변 조건

- Training과 평가 Dataset의 누수 검증이 필요합니다.
- metric version이나 checkpoint가 달라지면 새 EvaluationRun입니다.
- `completed`와 `approval=approved`는 별도 상태이며 `completed + pending/rejected`도 유효합니다.
- human review가 필수인 capability는 metric만으로 승인할 수 없습니다.
- similarity 결과는 창작 지원 위험 신호이며 법률 승인을 대체하지 않습니다.
- terminal 실행 record를 제자리 덮어쓰지 않습니다. rubric, metric, checkpoint 또는 approval evidence를 바꿔 재평가하면 새 EvaluationRun을 발급합니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | TrainingRun·metric·human review·approval 분리 정의 |
