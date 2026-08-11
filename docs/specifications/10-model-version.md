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
| `status` | `draft`, `evaluated`, `approved`, `runtime_allowed`, `deprecated` |
| `base` | base model ID·revision·license·checksum |
| `adapter` | optional adapter ID·format·checksum |
| `training_run_id` | 생성 학습 실행; 외부 base는 예외 사유 |
| `evaluation_run_ids` | 승인 판단 근거 |
| `model_manifest_id` | 대응하는 발행된 immutable ModelManifest |
| `rights_policy_eligibility_id` | 현재 권리·사용 정책 재평가 evidence |
| `supported_capability_ids` | 제공 capability |
| `runtime` | framework·precision·device·compatibility contract |
| `approval` | `pending`, `approved`, `rejected`와 evidence |
| `runtime_allowed` | Provider Runtime 승격 허용 |
| `deprecated` | 신규 선택 중단 여부 |
| `superseded_by` | 대체 version |
| `artifact_manifest_ids` | weight/tokenizer/config artifact |

`schema_name`은 `model_version`입니다.

## 3. 불변 조건

- `runtime_allowed=true`는 독립 설정값이 아니라 아래 조건의 파생 Gate입니다.
- 연결된 EvaluationRun이 존재하고 `status=completed`, `approval=approved`여야 합니다.
- ModelVersion의 `approval=approved`, `status=runtime_allowed`, `deprecated=false`여야 합니다.
- 대응 ModelManifest가 존재하고 완전성·checksum/digest 검증이 valid여야 합니다.
- base model, adapter, tokenizer, config, dependency와 대상 Provider Runtime compatibility가 모두 확인되고 pass여야 합니다.
- 현재 RightsMetadata·사용 정책이 eligible이며 `unknown`, `missing`, `expired`, `revoked`가 없어야 합니다.
- DatasetManifest → TrainingRun → EvaluationRun → ModelVersion → ModelManifest lineage가 완전해야 합니다.
- 위 조건 중 하나라도 거짓이면 `runtime_allowed=false`로 fail closed합니다.
- deprecated version은 신규 Job에 선택하지 않지만 재현·rollback을 위해 보존합니다.
- weight, tokenizer, adapter 또는 runtime compatibility 변경은 새 model version입니다.
- runtime 상태가 모델의 evaluation/rights 상태를 소급 변경하지 않습니다.
- 승인된 ModelVersion을 제자리 덮어쓰지 않습니다. 권리·정책 변경 후 Runtime 중단은 append-only event, eligibility 재평가와 필요 시 `supersedes` ModelVersion으로 기록합니다.
- `evaluated`, `approved`, `runtime_allowed`, `deprecated` 전이는 append-only status/eligibility event로 기록하고 current status는 그 projection입니다. 승인 payload 자체를 수정하지 않습니다.

금지 조합은 `runtime_allowed=true`와 EvaluationRun 미존재/미완료/미승인, ModelVersion 미승인, Manifest 미존재/무결성 실패, compatibility 미검증/실패, 권리 unknown/missing/expired/revoked 또는 `deprecated=true`의 모든 조합입니다.

```text
runtime_allowed = true IFF
  EvaluationRun.status = completed
  AND EvaluationRun.approval = approved
  AND ModelVersion.approval = approved
  AND ModelVersion.status = runtime_allowed
  AND ModelManifest exists
  AND ModelManifest integrity = valid
  AND runtime compatibility = pass
  AND current rights/policy eligibility = eligible
  AND deprecated = false
```

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | base·adapter·evaluation·runtime·deprecated 모델 identity 정의 |
