# DohaStudio Organization Contracts

이 Repository는 DohaStudio AI Music Ecosystem의 공통 문서와 Repository 간 계약을 관리합니다.

이번 기준 문서의 핵심은 DohaLM, DohaMusic, DohaAudio와 DohaVocal이 공유하는 AI Music Common Contracts입니다. 실제 Provider Runtime, Training, Inference, Dataset, REST, Streaming, Worker, Job과 DB 구현은 각 Repository의 책임이며 이 Repository에는 추가하지 않습니다.

## 문서

1. [문서 인덱스](docs/index.md)
2. [AI Music Common Contracts](docs/ai-music-common-contracts.md)
3. [Specification Index](docs/specifications/README.md)
4. [Common Contract Architecture](docs/architecture/common-ai-contracts.md)
5. [Roadmap](docs/roadmap.md)
6. [ADR Index](docs/decisions/README.md)
7. [문서 정합성 검토](docs/validation/common-ai-contracts-validation.md)

## 핵심 안전 경계

- Reference Audio를 직접 학습하지 않습니다.
- 학습은 승인된 FeatureRecord, 사용자 작업·수정·선택을 기반으로 합니다.
- SimilarityReport는 창작 지원 분석이며 법적 판정이 아닙니다.
- `approved`, `training_allowed`, `runtime_allowed`는 서로 다른 Gate입니다.
