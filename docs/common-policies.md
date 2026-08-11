# 공통 정책

> 문서 상태: [제안]

- AssetVersion은 불변이며 처리 결과는 새 파생 version입니다.
- Artifact는 ID, type, version, checksum, producer와 lineage를 기록합니다.
- ModelVersion이 모델 lifecycle·approval·Runtime Gate의 논리 권위이며 ModelManifest는 모델·Checkpoint·Dataset·Training·Evaluation·License·checksum을 고정한 발행 후 immutable evidence입니다.
- DatasetVersion이 Dataset lifecycle·approval·집합 eligibility·split·freeze의 논리 권위이며 DatasetManifest는 실제 포함 항목·split·Artifact·checksum을 고정한 발행 후 immutable evidence입니다.
- Manifest는 Version approval을 독립 변경하지 않으며 변경 시 새 Version/Manifest 또는 `supersedes` replacement를 발급하고 기존 record를 보존합니다.
- Provider Contract는 versioned job, status, cancel, retry, error와 result를 표현합니다.
- Dataset·모델·생성 결과의 Commercial Review를 분리합니다.
- Dataset, Checkpoint, 개인 음성과 Private Metadata를 Public Git에 포함하지 않습니다.
- 미구현 상태는 `[계획]`, `[검증 필요]`, `[미구현]`, `[Legacy]`, `[제안]`으로 표시합니다.
