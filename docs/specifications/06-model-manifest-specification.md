# 06. Model Manifest 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어
> 공통 Model Registry: [미구현]

## 1. 목적

ModelManifest는 권위 [ModelVersion](10-model-version.md)의 물리적 배포 구성을 재현하는 불변 직렬화 evidence입니다. weight, adapter, tokenizer, config, Runtime dependency, Artifact reference와 checksum/digest를 연결하며 ModelVersion과 경쟁하는 approval·lifecycle source of truth가 아닙니다.

## 2. 최소 필드

| 필드 | 의미 |
|---|---|
| `model_manifest_id` | immutable Manifest ID |
| `manifest_status` | 발행 전 `draft` 또는 terminal `issued` |
| `manifest_format_version` | 직렬화 형식 version |
| `source_model_version_id` | 권위 ModelVersion stable ID |
| `source_model_version_checksum` | Version/Manifest 결속 digest |
| `producer` | 생성 도구·version |
| `provider_id` | 모델을 제공하는 Provider |
| `model_id` | 모델 논리 식별자 |
| `model_version` | 모델 version |
| `checkpoint_version` | Checkpoint 또는 weight version |
| `model_type` | 생성·분석·변환 등 모델 유형 |
| `capabilities` | 지원 capability 목록 |
| `input_formats` | 지원 입력 형식 |
| `output_formats` | 지원 출력 형식 |
| `api_contract_version` | 호환 Provider 계약 version |
| `dataset_manifest_id` | 학습 Dataset Manifest |
| `training_run_id` | Training 또는 Fine-tuning Run |
| `evaluation_run_ids` | source ModelVersion의 승인 근거 EvaluationRun |
| `license_status` | 코드·weight license 검토 상태 |
| `commercial_usage_status` | 상업 이용 검토 상태 |
| `recommended_vram` | 실제 측정된 권장 VRAM |
| `runtime_environment` | Framework·CUDA·주요 의존성 version |
| `artifact_checksum` | Model Artifact checksum |
| `manifest_checksum` | canonical Manifest payload checksum |
| `supersedes` | 공식 replacement가 대체하는 이전 Manifest ID |
| `created_at` | Manifest 생성 시각 |

Provider별로 `supported_languages`, `voice_identity_scope`, `consent_requirement` 같은 확장 필드를 추가할 수 있습니다. 확장 필드는 namespace 또는 schema version으로 충돌을 방지합니다.

## 3. 상태 원칙

- 확인되지 않은 상태는 `UNKNOWN` 또는 `REVIEW_REQUIRED`로 기록합니다.
- 코드 license, weight license, Dataset license와 상업 이용 승인을 분리합니다.
- 실제 측정 없이 `recommended_vram`을 추정하지 않습니다.
- Evaluation 완료가 Commercial approval을 자동으로 의미하지 않습니다.
- Manifest에 기록된 approval·rights 값은 source ModelVersion과 evidence의 발행 시점 snapshot이며 독립 변경 권한이 없습니다.

## 4. 경로와 Artifact

Manifest에 로컬 절대 경로를 저장하지 않습니다. 모델과 Checkpoint는 [Artifact](03-artifact-specification.md) ID와 checksum으로 참조합니다. 필요한 base model, weight, adapter, tokenizer, config와 dependency가 모두 검증 가능해야 합니다.

## 5. 변경과 폐기

`draft`는 발행 전 검토 중에만 변경할 수 있습니다. `issued` ModelManifest는 terminal immutable record입니다. payload, weight·adapter·tokenizer·config·dependency·Artifact reference, checksum/digest 또는 source ModelVersion 중 하나라도 달라지면 같은 Manifest ID를 유지할 수 없습니다.

물리 구성이나 Model 의미가 바뀌면 새 ModelVersion과 새 ModelManifest를 발급합니다. 논리 ModelVersion은 같지만 발행 evidence 오류를 정정해야 하는 예외는 새 Manifest ID와 canonical `supersedes` 관계를 사용하며 source ModelVersion approval을 변경할 수 없습니다. 기존 Version·Manifest를 삭제하거나 덮어쓰지 않습니다.

## 관련 명세

- [Provider 계약](04-provider-contract.md)
- [Dataset Manifest 명세](07-dataset-manifest-specification.md)
- [Storage Layout 명세](09-storage-layout-specification.md)
