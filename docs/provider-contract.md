# 공통 Provider 계약

> 문서 상태: [제안]
> Provider HTTP API: Repository별 [계획] 또는 [미구현]

공통 Provider 기능 후보는 Capabilities, Create Job, Get Status, Cancel, Retry, Get Result, Get Model Manifest, Health와 Readiness입니다.

## 원칙

- DohaMusic만 Provider를 호출합니다.
- Provider끼리는 직접 호출하지 않습니다.
- 계약과 오류에는 version을 지정합니다.
- 장기 작업은 비동기 Job으로 처리합니다.
- 결과는 로컬 절대 경로가 아니라 Artifact ID·URI와 checksum으로 전달합니다.
- 사용자 권한, Provider 순서와 GPU admission은 DohaMusic이 관리합니다.

세부 Job 상태, 오류 schema와 transport는 각 Provider 계약과 통합 검증 후 확정합니다.
