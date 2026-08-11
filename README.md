# DohaStudio 조직 문서 저장소

> 문서 상태: [제안]
> 공통 명세: `0.1.0` (`draft-baseline`)

이 Public `.github` 저장소는 DohaStudio AI Music Ecosystem의 Organization Profile, 공통 Architecture, Repository 관계, 개발·보안·라이선스 정책과 Contribution 기준을 관리합니다.

실제 Organization 첫 화면은 [profile/README.md](profile/README.md)가 `main`에 반영된 뒤 표시됩니다. 현재 문서는 Draft PR 검토 대상이며 Runtime, Dataset, Training 또는 Repository Migration을 포함하지 않습니다.

## 주요 문서

- [DohaStudio Organization Profile](profile/README.md)
- [문서 인덱스](docs/index.md)
- [Ecosystem Overview](docs/ecosystem-overview.md)
- [Repository Boundary](docs/repository-boundary.md)
- [Provider Contract](docs/provider-contract.md)
- [Common Policies](docs/common-policies.md)
- [공통 명세 기준선](docs/specifications/README.md)
- [AI Music Common Contracts](docs/ai-music-common-contracts.md)
- [Common Contract Architecture](docs/architecture/common-ai-contracts.md)
- [Common Contract ADR](docs/decisions/README.md)
- [Common Contract 정합성 검토](docs/validation/common-ai-contracts-validation.md)
- [변경 이력](CHANGELOG.md)
- [Contribution](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Support](SUPPORT.md)

## 저장소

- [DohaMusic](https://github.com/DohaStudio/DohaMusic)
- [DohaLM](https://github.com/DohaStudio/DohaLM)
- [DohaAudio](https://github.com/DohaStudio/DohaAudio)
- [DohaVocal](https://github.com/DohaStudio/DohaVocal)

모든 기능 상태는 각 Repository 문서를 기준으로 판단합니다. Organization 문서는 구현되지 않은 Runtime·Provider 기능을 완료된 것으로 표시하지 않습니다.

## Common Contract 안전 경계

- Reference Audio를 직접 학습하지 않습니다.
- 학습은 승인된 FeatureRecord와 사용자 작업·수정·선택을 기반으로 합니다.
- SimilarityReport는 창작 지원 분석이며 법적 판정이 아닙니다.
- `training_allowed`와 `ModelVersion.runtime_allowed`는 서로 다른 Gate입니다.
