# Security Policy

## 공개 Issue에 올리지 않을 내용

- 비밀정보, token과 credential
- 개인 음성, Recording, Consent 증적과 실제 경로
- Dataset·AIHub package·Checkpoint·모델 weight
- Private Metadata와 재현 가능한 공격 세부정보

## 취약점 신고

공개 Issue 대신 GitHub Repository의 Security Advisories에서 비공개 보고 기능을 사용할 수 있는지 먼저 확인해 주세요. 사용할 수 없다면 민감 내용을 공개하지 말고 Organization 관리자에게 안전한 연락 경로를 요청해 주세요.

신고에는 영향받는 Repository·version, 영향, 최소 재현 조건과 완화 제안을 포함하되 실제 개인 데이터는 첨부하지 않습니다.

## 범위

보안 정책은 코드뿐 아니라 Provider 인증, Artifact 접근, Dataset 권리, 개인 음성, 사용자별 Adapter와 Checkpoint의 음성 정체성 위험을 포함합니다.
