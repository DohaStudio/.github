# Common Policies

> 문서 상태: [제안]

- AssetVersion은 불변이며 처리 결과는 새 파생 version입니다.
- Artifact는 ID, type, version, checksum, producer와 lineage를 기록합니다.
- Model Manifest는 모델·Checkpoint·Dataset·Training·Evaluation·License 근거를 연결합니다.
- Dataset Manifest는 provenance, checksum, split, rights와 lifecycle을 기록합니다.
- Provider Contract는 versioned job, status, cancel, retry, error와 result를 표현합니다.
- Dataset·모델·생성 결과의 Commercial Review를 분리합니다.
- Dataset, Checkpoint, 개인 음성과 Private Metadata를 Public Git에 포함하지 않습니다.
- 미구현 상태는 `[계획]`, `[검증 필요]`, `[미구현]`, `[Legacy]`, `[제안]`으로 표시합니다.
