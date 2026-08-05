# 06. Model Manifest 공통 명세

> 상태: [제안]
> 공식 문서 언어: 한국어
> 공통 Model Registry: [미구현]

## 1. 목적

Model Manifest는 Provider Runtime이 사용하는 모델, Checkpoint, Dataset, Training, Evaluation, License와 실행 환경을 재현 가능한 식별자로 연결합니다.

## 2. 최소 필드

| 필드 | 의미 |
|---|---|
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
| `evaluation_result_id` | 승인 근거 Evaluation 결과 |
| `license_status` | 코드·weight license 검토 상태 |
| `commercial_usage_status` | 상업 이용 검토 상태 |
| `recommended_vram` | 실제 측정된 권장 VRAM |
| `runtime_environment` | Framework·CUDA·주요 의존성 version |
| `artifact_checksum` | Model Artifact checksum |
| `created_at` | Manifest 생성 시각 |

Provider별로 `supported_languages`, `voice_identity_scope`, `consent_requirement` 같은 확장 필드를 추가할 수 있습니다. 확장 필드는 namespace 또는 schema version으로 충돌을 방지합니다.

## 3. 상태 원칙

- 확인되지 않은 상태는 `UNKNOWN` 또는 `REVIEW_REQUIRED`로 기록합니다.
- 코드 license, weight license, Dataset license와 상업 이용 승인을 분리합니다.
- 실제 측정 없이 `recommended_vram`을 추정하지 않습니다.
- Evaluation 완료가 Commercial approval을 자동으로 의미하지 않습니다.

## 4. 경로와 Artifact

Manifest에 로컬 절대 경로를 저장하지 않습니다. 모델과 Checkpoint는 [Artifact](03-artifact-specification.md) ID와 checksum으로 참조합니다. Artifact가 변경되면 기존 Manifest를 수정하지 않고 새 version을 발급합니다.

## 5. 변경과 폐기

Manifest는 게시 후 불변으로 취급합니다. 새 Checkpoint, 환경, Dataset 또는 License 판단은 새 Manifest version을 만듭니다. 폐기된 모델은 삭제 대신 상태와 대체 Manifest를 기록합니다.

## 관련 명세

- [Provider 계약](04-provider-contract.md)
- [Dataset Manifest 명세](07-dataset-manifest-specification.md)
- [Storage Layout 명세](09-storage-layout-specification.md)
