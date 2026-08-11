# ModelVersion Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`ModelVersion`은 base model과 선택적 adapter, Training/Evaluation lineage, Runtime compatibility를 연결하는 불변 모델 identity입니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `model_id` | 논리 model ID |
| `model_version` | 불변 version |
| `base` | base model ID·revision·license·checksum |
| `adapter` | optional adapter ID·format·checksum |
| `training_run_id` | 생성 학습 실행; 외부 base는 예외 사유 |
| `evaluation_run_ids` | 승인 판단 근거 |
| `supported_capability_ids` | 제공 capability |
| `runtime` | framework·precision·device·compatibility contract |
| `approved` | 모델 사용 승인 |
| `runtime_allowed` | Provider Runtime 승격 허용 |
| `deprecated` | 신규 선택 중단 여부 |
| `superseded_by` | 대체 version |
| `artifact_manifest_ids` | weight/tokenizer/config artifact |

`schema_name`은 `model_version`입니다.

## 3. 불변 조건

- base와 adapter compatibility가 검증돼야 합니다.
- `approved=true`, `runtime_allowed=true`, 권리·evaluation Gate가 모두 필요합니다.
- deprecated version은 신규 Job에 선택하지 않지만 재현·rollback을 위해 보존합니다.
- weight, tokenizer, adapter 또는 runtime compatibility 변경은 새 model version입니다.
- runtime 상태가 모델의 evaluation/rights 상태를 소급 변경하지 않습니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | base·adapter·evaluation·runtime·deprecated 모델 identity 정의 |
