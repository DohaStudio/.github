# ProviderCapability Specification

> 상태: [제안]
> 마지막 검토일: 2026-08-11

## 1. 역할

`ProviderCapability`는 DohaLM, DohaAudio와 DohaVocal이 제공하는 기능, 입출력 계약과 지원 version을 선언합니다. DohaMusic은 이를 조회해 orchestration합니다.

## 2. 필드

| 필드 | 의미 |
|---|---|
| `provider_id` | `dohalm`, `dohaaudio`, `dohavocal` 등 |
| `capability_id` | 안정적인 기능 ID |
| `capability_version` | 의미·입출력 contract version |
| `input_schema_refs` | 지원 입력 schema/version |
| `output_schema_refs` | 지원 출력 schema/version |
| `supported_operations` | MusicIntent operation subset |
| `execution_mode` | sync/async/streaming 선언 |
| `model_version_ids` | 선택 가능한 승인 모델 |
| `constraints` | duration, format, device, rights 등 |
| `status` | `planned`, `available`, `degraded`, `unavailable`, `deprecated` |

`schema_name`은 `provider_capability`입니다.

## 3. 공통 Capability ID

| Provider | Capability |
|---|---|
| DohaLM | `lyrics_generation`, `lyrics_rewrite`, `planning`, `prompt_generation`, `music_qa`, `similarity_interpretation` |
| DohaAudio | `music_generation`, `stem_separation`, `audio_analysis`, `similarity_analysis`, `mix_processing` |
| DohaVocal | `voice_conversion`, `singing`, `vocal_analysis`, `vocal_edit` |

## 4. 불변 조건

- Provider끼리 직접 호출하지 않고 DohaMusic이 orchestration합니다.
- 지원하지 않는 schema major version·operation은 명시적으로 거부합니다.
- `available`은 권리·모델·runtime readiness가 모두 유효한 상태여야 합니다.
- capability 목록은 실제 구현 상태를 과장하지 않습니다.
- capability ID 의미 변경은 새 major version 또는 새 ID를 사용합니다.

## 변경 이력

| 날짜 | 변경 내용 |
|---|---|
| 2026-08-11 | 세 Provider의 capability discovery·schema·status 계약 정의 |
